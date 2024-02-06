import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta


def add_buildings():
    Building.objects.create(
        name="Научно-образовательный корпус",
        description="2-я Бауманская улица, 7с1",
        floors=5,
        year=2020,
        image="buildings/1.png"
    )

    Building.objects.create(
        name="Квантум парк",
        description="Бригадирский переулок, 13с4",
        floors=6,
        year=2021,
        image="buildings/2.png"
    )

    Building.objects.create(
        name="Библиотечный корпус",
        description="2-я Бауманская улица, 10",
        floors=3,
        year=2023,
        image="buildings/3.png"
    )

    Building.objects.create(
        name="Дворец технологий",
        description="Бауманская улица, 57Ас1",
        floors=8,
        year=2024,
        image="buildings/4.png"
    )

    Building.objects.create(
        name="Центр биомедицинских систем и технологий",
        description="Бригадирский переулок, 12",
        floors=6,
        year=2022,
        image="buildings/5.png"
    )

    Building.objects.create(
        name="Комплекс общежитий",
        description="2-я Бауманская улица, 13",
        floors=15,
        year=2021,
        image="buildings/6.png"
    )

    print("Услуги добавлены")


def add_verifications():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    buildings = Building.objects.all()

    for _ in range(30):
        verification = Verification.objects.create()
        verification.status = random.randint(2, 5)
        verification.owner = random.choice(owners)

        if verification.status in [3, 4]:
            verification.date_complete = random_date()
            verification.date_formation = verification.date_complete - random_timedelta()
            verification.date_created = verification.date_formation - random_timedelta()
            verification.moderator = random.choice(moderators)
        else:
            verification.date_formation = random_date()
            verification.date_created = verification.date_formation - random_timedelta()

        for building in buildings.order_by('?')[:3]:
            item = BuildingVerification.objects.create()
            item.verification = verification
            item.building = building
            item.state = random.randint(0, 100)
            item.save()

        verification.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_buildings()
        add_verifications()









