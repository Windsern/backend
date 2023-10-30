from django.db import models
from enum import Enum

# Create your models here.
class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True, serialize=False)
    login = models.CharField(max_length=31)
    password = models.CharField(max_length=31)
    is_admin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'

# class BuildingStatus(Enum):
#     Deleted = "Удалён"
#     Active = "Действует"


class Building(models.Model):
    building_id = models.BigAutoField(primary_key=True, serialize=False)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type_building = models.CharField(max_length=127)
    count_floor = models.IntegerField()
    year_building = models.IntegerField()
    document_building = models.CharField(max_length=10)
    project_document = models.CharField(max_length=10)
    status_building = models.CharField(max_length=15)
    # status = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in BuildingStatus])
    # status = models.CharField(max_length=15, choices=[
    #     ("Deleted", "Удалён"),
    #     ("Active", "Действует"),
    # ])
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'building'

class CheckingStatus(Enum):
    Entered = "Введён"
    Progress = "В работе"
    Completed = "Завершён"
    Canceled = "Отменён"
    Deleted = "Удалён"

class Checking(models.Model):
    checking_id = models.BigAutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=127)
    age = models.IntegerField()
    status = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in CheckingStatus])

    user_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='user_id',  # Имя поля в базе данных
    )

    # building_id = models.ForeignKey(
    #     Building,
    #     on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
    #     db_column='building_id',  # Имя поля в базе данных
    # )

    publication_date = models.DateField()
    creation_time = models.DateField()
    approving_date = models.DateField()
    moderator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='moderator',  # Имя поля в базе данных
        related_name='moderator_user_id'
    )

    class Meta:
        managed = False
        db_table = 'checking'


class CheckingsBuildings(models.Model):
    # id = models.BigAutoField(primary_key=True, serialize=False)
    building_id = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='building_id',  # Имя поля в базе данных
    )
    checking_id = models.ForeignKey(
        Checking,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='checking_id',  # Имя поля в базе данных
    )
    class Meta:
        managed = False
        db_table = 'checkingsbuildings'