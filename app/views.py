from django.db import connection
from django.shortcuts import render, redirect

from .models import *


def get_draft_order():
    return Verification.objects.filter(status=1).first()


def index(request):
    query = request.GET.get("query", "")
    buildings = Building.objects.filter(name__icontains=query).filter(status=1)
    draft_order = get_draft_order()

    context = {
        "query": query,
        "buildings": buildings,
        "draft_order_id": draft_order.pk if draft_order else None
    }

    return render(request, "home_page.html", context)


def building_details(request, building_id):
    context = {
        "building": Building.objects.get(id=building_id)
    }

    return render(request, "building_page.html", context)


def building_delete(request, building_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE app_building SET status = 2 WHERE id = %s", [building_id])

    return redirect("/")


def get_buildings(verification):
    items = BuildingVerification.objects.filter(verification=verification)
    return [item.building for item in items]


def order_details(request, order_id):
    verification = Verification.objects.get(id=order_id)

    context = {
        "verification": verification,
        "buildings": get_buildings(verification)
    }

    return render(request, "order_page.html", context)


def building_add_to_order(request, building_id):
    building = Building.objects.get(pk=building_id)

    verification = get_draft_order()

    if verification is None:
        verification = Verification.objects.create()

    item = BuildingVerification.objects.create()
    item.verification = verification
    item.building = building
    item.save()

    return redirect("/")


def order_delete(request, order_id):
    verification = Verification.objects.get(pk=order_id)
    verification.status = 5
    verification.save()
    return redirect("/")

