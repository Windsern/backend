from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.db import connection
from .database import Database
from .models import Building
from datetime import date
# from django.contrib import messages
# from django.shortcuts import get_object_or_404

database_ = [
    {'id': 1, 'title': 'Научно-образовательный корпус', 'address': '2-я Бауманская улица, 7с1',
     'type_building': 'Общественный', 'count_floor': 5, 'year_building': 2020, 'document_building': 'Да',
     'project_document': 'Да', 'status': 'Строится'},
    {'id': 2, 'title': 'Квантум парк', 'address': 'Бригадирский переулок, 13с4', 'type_building': 'Общественный',
     'count_floor': 5, 'year_building': 2020, 'document_building': 'Да', 'project_document': 'Да',
     'status': 'Строится'},
    {'id': 3, 'title': 'Дом РФ', 'address': 'Бригадирский переулок, 12с1', 'type_building': 'Общественный',
     'count_floor': 5, 'year_building': 2020, 'document_building': 'Да', 'project_document': 'Да',
     'status': 'Построен'},
    {'id': 4, 'title': 'Образовательный комплекс', 'address': 'Бригадирский переулок, 13',
     'type_building': 'Общественный', 'count_floor': 5, 'year_building': 2020, 'document_building': 'Да',
     'project_document': 'Да', 'status': 'Строится'},
    {'id': 5, 'title': 'Библиотечный корпус', 'address': '2-я Бауманская улица, 10', 'type_building': 'Общественный',
     'count_floor': 5, 'year_building': 2020, 'document_building': 'Да', 'project_document': 'Да',
     'status': 'Строится'},
    {'id': 6, 'title': 'Дворец технологий', 'address': 'Бауманская улица, 57Ас1', 'type_building': 'Общественный',
     'count_floor': 5, 'year_building': 2020, 'document_building': 'Да', 'project_document': 'Да',
     'status': 'Строится'},
    {'id': 7, 'title': 'Центр биомедицинских систем и технологий', 'address': 'Бригадирский переулок, 12',
     'type_building': 'Общественный', 'count_floor': 5, 'year_building': 2020, 'document_building': 'Да',
     'project_document': 'Да', 'status': 'Строится'},
    {'id': 8, 'title': 'Комплекс общежитий', 'address': '55.771550, 37.695786', 'type_building': 'Общественный',
     'count_floor': 20, 'year_building': 2020, 'document_building': 'Да', 'project_document': 'Да',
     'status': 'Строится'},
    {'id': 9, 'title': 'Образовательно-досуговый центр Спектр', 'address': '55.771777, 37.695370',
     'type_building': 'Общественный', 'count_floor': 20, 'year_building': 2020, 'document_building': 'Да',
     'project_document': 'Да', 'status': 'Строится'},
]


def GetBuilds(request):
    building_keyword = request.GET.get('building_keyword')

    if building_keyword is None or building_keyword == '':
        buildings = Building.objects.filter(status=True)
        return render(request, 'orders.html', {'data': {
            'builds': buildings
        }})

    else:
        buildings = Building.objects.filter(title=building_keyword, status=True)
        return render(request, 'services.html', {'data': {
            'building_keyword': building_keyword,
            'builds': buildings
        }})

def GetBuild(request, id):
    # Найдем объект в списке по 'id'
    # builds = Building.objects
    # order = None
    # for obj in builds:
    #     if obj['id'] == id:
    #         order = obj
    #         break
    #
    # if order is None:
    #     raise Http404("Объект не найден")
    #
    # return render(request, 'order.html', {'data': {
    #     'current_date': date.today(),
    #     # 'order': order,
    #     'build': order
    #     # 'build': builds
    # }})

    try:
        build = Building.objects.get(building_id=id, status=True)
    except Building.DoesNotExist:
        raise Http404("Объект не найден")

    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'build': build,
    }})

def building(request):
    building_keyword = request.GET.get('building_keyword')

    # Преобразовать ключевое слово в строку для поиска в базе данных
    building_keyword = str(building_keyword)

    if building_keyword == "None" or building_keyword == '':
        # bld = Building.objects.filter(status=BuildingStatus.Active)
        #
        # return render(request, 'orders.html', {'data': {
        #     'builds': bld
        # }})

        return render(request, 'orders.html', {'data': {
            'current_date': date.today(),
            'builds': database_
        }})

    else:
        # bld = Building.objects.filter(title=building_keyword, status=BuildingStatus.Active)

        # Получить список услуг из базы данных
        building_services = []

        building_services = [
            service for service in database_
            if building_keyword.lower() == service['title'].lower()
        ]

        return render(request, 'services.html', {'building_keyword': building_keyword, 'builds': building_services})
        # return render(request, 'services.html', {'data': {
        #     'building_keyword': building_keyword,
        #     'builds': bld
        # }})

def delete_building(request):
    if request.method == 'POST':
        # Получаем значение city_id из POST-запроса
        building_id = request.POST.get('building_id')
        building_id = int(building_id)

        if (building_id is not None):
            # Выполняем SQL запрос для редактирования статуса
            DB = Database()

            DB.connect()
            DB.update_status(status=False, id_building=building_id)
            DB.close()
        # Перенаправим на предыдующую ссылку после успешного удаления
        return redirect('http://127.0.0.1:8000/')


# from bmstu_lab.models import Book
#
# def bookList(request):
#     return render(request, 'books.html', {'data' : {
#         'current_date': date.today(),
#         'books': Book.objects.all()
#     }})
#
# def GetBook(request, id):
#     return render(request, 'book.html', {'data' : {
#         'current_date': date.today(),
#         'book': Book.objects.filter(id=id)[0]
#     }})
#
#
# book = Book.objects.all()
# print(book.query)
#
# # получаем объекты с именем Tom
# book = book.filter(name="Tom")
# print(book.query)

# получаем объекты с возрастом, равным 31
# book = book.filter(age=31)
# print(book.query)

# здесь происходит выполнения запроса в БД
# for Book in book:
#     print(f"{Book.id}.{Book.name} - {Book.description}")
