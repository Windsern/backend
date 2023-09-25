from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import date

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
    return render(request, 'orders.html', {'data': {
        'current_date': date.today(),
        'builds': database_
    }})


def GetBuild(request, id):
    # Найдем объект в списке по 'id'
    order = None
    for obj in database_:
        if obj['id'] == id:
            order = obj
            break

    if order is None:
        raise Http404("Объект не найден")

    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'build': order
    }})


def building(request):
    building_keyword = request.GET.get('building_keyword')

    # Преобразовать ключевое слово в строку для поиска в базе данных
    building_keyword = str(building_keyword)

    # Получить список услуг из базы данных
    building_services = []

    building_services = [
        service for service in database_
        if building_keyword.lower() == service['title'].lower()
    ]

    return render(request, 'services.html', {'database_': building_services})
