from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
# from drf_yasg.utils import swagger_auto_schema
# ---- rest-api ----
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# from .jwt_helper import create_access_token
# from .permissions_s import *
from .serializers import *
from .models import *

# access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()

@api_view(["GET"])
def search_building(request):
    """
    Возвращает список строений
    """

    def get_draft_checking_id():
        checking = Checking.objects.filter(status=1).first()

        if checking is None:
            return None

        return checking.checking_id

    # query = request.GET.get("query", "")

    # Получим параметры запроса из URL
    title = request.GET.get('title')
    address = request.GET.get('address')
    type_building = request.GET.get('type_building')
    count_floor = request.GET.get('count_floor')
    year_building = request.GET.get('year_building')
    document_building = request.GET.get('document_building')
    project_document = request.GET.get('project_document')
    status_building = request.GET.get('status_building')
    status = request.GET.get('status')

    # Получение данные после запроса с БД (через ORM)
    building = Building.objects.filter(status=1)

    # Для лабораторной работы №3
    # if title:
    #     building = building.filter(title__icontains=title)

    if title and address and type_building and count_floor and year_building and document_building and project_document\
            and status_building and status is None:
        pass
    else:
        # Применим фильтры на основе параметров запроса, если они предоставлены
        if title:
            building = building.filter(title__icontains=title)
        if address:
            building = building.filter(address__icontains=address)
        if type_building:
            building = building.filter(type_building__icontains=type_building)
        if count_floor:
            building = building.filter(count_floor=count_floor)
        if year_building:
            building = building.filter(year_building=year_building)
        if document_building:
            building = building.filter(document_building__icontains=document_building)
        if project_document:
            building = building.filter(project_document__icontains=project_document)
        if status_building:
            building = building.filter(status_building__icontains=status_building)
        if status:
            building = building.filter(status=status)



    serializer = BuildingSerializer(building, many=True)

    return Response(serializer.data)

    # Для лабораторной работы №3
    # resp = {
    #     "draft_checking": get_draft_checking_id(),
    #     "checkings": serializer.data
    # }

    # return Response(resp)


@api_view(['GET'])
def get_building_by_id(request, building_id):
    """
    Возвращает информацию о конкретном строении
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Получение данные после запроса с БД (через ORM)
    building = Building.objects.get(pk=building_id)

    serializer = BuildingSerializer(building, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_building(request, building_id):
    """
    Обновляет информацию о строении
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    serializer = BuildingSerializer(building, data=request.data, partial=True)

    if serializer.is_valid():
        building.status = 1
        building.save()
        serializer.save()
        # serializer.status = 1
        # serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def create_building(request):
    """
    Добавляет новое строение
    """
    Building.objects.create()

    # building = Building.objects.filter(status='null').last()
    # building.status = 'True'
    # building.save()

    # building = Building.objects.filter().last()
    #
    # if building:
    #     building.status = 1  # Используйте True, не 'True'
    #     building.save()

    building = Building.objects.all()
    serializer = BuildingSerializer(building, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_building(request, building_id):
    """
    Удаляет строение
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    # serializer = BuildingSerializer(building, data=request.data, partial=True)

    building.status = 2
    building.save()

    buildings = Building.objects.filter(status=1)
    serializer = BuildingSerializer(buildings, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_building_to_checking(request, building_id):
    """
    Добавляет строение в заявку
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)

    # draft_estimate = get_draft_checking_id()

    checking = Checking.objects.filter(status=1).last()
    # print(checking.title)

    # if checking is None:
    #     checking = Checking.objects.create(creation_time=datetime.now(timezone.utc), approving_date=None,
    #                                        publication_date=None)
    #     if checking.status == 1:
    #         if checking.users is None:
    #             try:
    #                 new_user = Users.objects.create(login="user1")
    #             except IntegrityError:
    #                 # User with login "user1" already exists, get the existing user
    #                 new_user = Users.objects.get(login="user1")
    #             checking.users = new_user
    #             checking.save()


    checking.buildings.add(building)
    checking.save()

    # cities - это cities = models.ManyToManyField(City, verbose_name="Города", null=True)
    serializer = CheckingSerializer(checking, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_building_image(request, building_id):
    """
    Возвращает фото строения
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Building.objects.get(pk=building_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_building_image(request, building_id):
    """
    Обновляет фото города
    """
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    building.image = request.data.get("image")
    print(request.data)
    print(building.image)

    serializer = BuildingSerializer(building, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_checkings(request):
    """
    Возвращает список заявок
    """
    checkings = Checking.objects.all()

    # Получим параметры запроса из URL
    status = request.GET.get('status')
    creation_time = request.GET.get('creation_time')
    publication_date = request.GET.get('publication_date')
    date_form_after = request.GET.get('date_form_after')
    date_form_before = request.GET.get('date_form_before')

    # Применим фильтры на основе параметров запроса, если они предоставлены
    if status:
        checkings = checkings.filter(status=status)
    if creation_time:
        checkings = checkings.filter(creation_time=creation_time)
    if publication_date:
        checkings = checkings.filter(publication_date=publication_date)

    # Дата формирования ПОСЛЕ
    if date_form_after and date_form_before is None:
        checkings = checkings.filter(date_of_formation__gte=date_form_after)
    # Дата формирования ДО
    if date_form_after is None and date_form_before:
        checkings = checkings.filter(date_of_formation__lte=date_form_before)

    # Дата формирования ПОСЛЕ и ДО
    if date_form_after and date_form_before:
        if date_form_after > date_form_before:
            return Response('Mistake! It is impossible to sort when "BEFORE" exceeds "AFTER"!')
        checkings = checkings.filter(date_of_formation__gte=date_form_after, date_of_formation__lte=date_form_before)

    serializer = CheckingSerializer(checkings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_checking_by_id(request, checking_id):
    """
    Возвращает информацию о конкретной заявке
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    checking = Checking.objects.get(pk=checking_id)
    serializer = CheckingSerializer(checking, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_checking(request, checking_id):
    """
    Обновляет информацию о заявке
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    checking = Checking.objects.get(pk=checking_id)
    serializer = CheckingSerializer(checking, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    checking.status = 1
    checking.save()

    return Response(serializer.data)


# +/-
@api_view(["PUT"])
def update_status_user(request, checking_id):
    """
    Пользователь обновляет информацию о вакансии
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    checking = Checking.objects.get(pk=checking_id)
    if checking.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        checking.status = 2
        checking.save()
        if checking.status == 2:
            checking.approving_date = datetime.now()
            checking.save()
            if checking.users is None:
                new_user = Users.objects.create(login="user1")
                checking.users = new_user
                checking.save()
            else:
                checking.users.login = "user1"
                checking.users.save()

    serializer = CheckingSerializer(checking, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, checking_id):
    """
    Модератор обновляет информацию о вакансии
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # request_status = request.data["status"]
    #
    # if request_status in [1, 5]:
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    # vacancy = Vacancy.objects.get(pk=vacancy_id)
    #
    # lesson_status = vacancy.status
    #
    # if lesson_status in [2, 3, 4, 5]:
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    # vacancy.status = request_status
    # vacancy.save()

    checking = Checking.objects.get(pk=checking_id)
    if checking.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        checking.status = 4
        checking.save()
        if checking.status == 4:
            checking.publication_date = datetime.now()
            checking.save()

    # request_status = request.data["status"]
    #
    # if request_status not in [3, 4]:
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    # vacancy = Vacancy.objects.get(pk=vacancy_id)
    #
    # vacancy_status = vacancy.status
    #
    # if vacancy_status != 2:
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    # vacancy.status = request_status
    # vacancy.save()

    serializer = CheckingSerializer(checking, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_checking(request, checking_id):
    """
    Удаляет заявку
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    checking = Checking.objects.get(pk=checking_id)

    if checking.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    checking.status = 5
    checking.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_building_from_checking(request, checking_id, building_id):
    """
    Удаляет строение из заявок
    """
    if not Checking.objects.filter(pk=checking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    checking = Checking.objects.get(pk=checking_id)
    checking.buildings.remove(Building.objects.get(pk=building_id))
    checking.save()

    serializer = BuildingSerializer(checking.buildings, many=True)

    return Response(serializer.data)

# @swagger_auto_schema(method='post', request_body=UserLoginSerializer)
# @api_view(["POST"])
# def login(request):
#     serializer = UserLoginSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

#     user = authenticate(**serializer.data)
#     if user is None:
#         message = {"message": "invalid credentials"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     access_token = create_access_token(user.id)

#     user_data = {
#         "user_id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "is_moderator": user.is_moderator,
#         "access_token": access_token
#     }

#     response = Response(user_data, status=status.HTTP_201_CREATED)

#     response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

#     return response


# @api_view(["POST"])
# def register(request):
#     serializer = UserLoginSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Check credentials
#     user = authenticate(**serializer.data)
#     if user is None:
#         message = {"message": "invalid credentials"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     access_token = create_access_token(user.id)

#     user_data = {
#         "user_id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "is_moderator": user.is_moderator,
#         "access_token": access_token
#     }
#     cache.set(access_token, user_data, access_token_lifetime)

#     response = Response(user_data, status=status.HTTP_201_CREATED)

#     response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

#     return response


# @api_view(["POST"])
# def check(request):
#     token = get_access_token(request)

#     if token is None:
#         message = {"message": "Token is not found"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     if token in cache:
#         message = {"message": "Token in blacklist"}
#         return Response(message, status=status.HTTP_401_UNAUTHORIZED)

#     payload = get_jwt_payload(token)
#     user_id = payload["user_id"]

#     user = Users.objects.get(pk=user_id)
#     serializer = UsersSerializer(user, many=False)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     access_token = get_access_token(request)

#     if access_token not in cache:
#         cache.set(access_token, access_token_lifetime)

#     message = {"message": "Вы успешно вышли из аккаунта"}
#     response = Response(message, status=status.HTTP_200_OK)

#     response.delete_cookie('access_token')

#     return response

def GetBuilds(request):
    building_keyword = request.GET.get('building_keyword')

    if building_keyword is None or building_keyword == '':
        buildings = Building.objects.filter(status=1)
        return render(request, 'orders.html', {'data': {
            'builds': buildings
        }})

    else:
        buildings = Building.objects.filter(title=building_keyword, status=1)
        return render(request, 'services.html', {'data': {
            'building_keyword': building_keyword,
            'builds': buildings
        }})


def GetBuild(request, id):
    try:
        build = Building.objects.get(building_id=id, status=1)
    except Building.DoesNotExist:
        raise Http404("Объект не найден")

    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'build': build,
    }})

# def building(request):
#     building_keyword = request.GET.get('building_keyword')
#
#     # Преобразовать ключевое слово в строку для поиска в базе данных
#     building_keyword = str(building_keyword)
#
#     if building_keyword == "None" or building_keyword == '':
#         # bld = Building.objects.filter(status=BuildingStatus.Active)
#         #
#         # return render(request, 'orders.html', {'data': {
#         #     'builds': bld
#         # }})
#
#         return render(request, 'orders.html', {'data': {
#             'current_date': date.today(),
#             'builds': database_
#         }})
#
#     else:
#         # bld = Building.objects.filter(title=building_keyword, status=BuildingStatus.Active)
#
#         # Получить список услуг из базы данных
#         building_services = []
#
#         building_services = [
#             service for service in database_
#             if building_keyword.lower() == service['title'].lower()
#         ]
#
#         return render(request, 'services.html', {'building_keyword': building_keyword, 'builds': building_services})
#         # return render(request, 'services.html', {'data': {
#         #     'building_keyword': building_keyword,
#         #     'builds': bld
#         # }})

# def delete_building(request):
#     if request.method == 'POST':
#         # Получаем значение city_id из POST-запроса
#         building_id = request.POST.get('building_id')
#         building_id = int(building_id)
#
#         if (building_id is not None):
#             # Выполняем SQL запрос для редактирования статуса
#             DB = Database()
#
#             DB.connect()
#             DB.update_status(status=False, id_building=building_id)
#             DB.close()
#         # Перенаправим на предыдующую ссылку после успешного удаления
#         return redirect('http://127.0.0.1:8000/')
