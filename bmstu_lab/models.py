from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.

# class UsersManager(BaseUserManager):
#     def create_user(self, name, email, password="1234", **extra_fields):
#         extra_fields.setdefault('name', name)
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, name, email, password="1234", **extra_fields):
#         extra_fields.setdefault('is_moderator', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(name, email, password, **extra_fields)


# class Users(AbstractBaseUser, PermissionsMixin):
class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True, serialize=False)
    login = models.CharField(max_length=31)
    password = models.CharField(max_length=31)
    is_admin = models.BooleanField()

    # email = models.EmailField(unique=True)
    # name = models.CharField(max_length=30)
    # is_moderator = models.BooleanField(default=False)

    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)

    # objects = UsersManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']

    class Meta:
        managed = False
        db_table = 'users'

class Building(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    building_id = models.BigAutoField(primary_key=True, serialize=False)
    title = models.CharField(max_length=255, verbose_name="Строение")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    type_building = models.CharField(max_length=127, verbose_name="Тип здания")
    count_floor = models.IntegerField(verbose_name="Количество этажей")
    year_building = models.IntegerField(verbose_name="Год постройки")
    document_building = models.CharField(max_length=10, verbose_name="Разрешение на строительство")
    project_document = models.CharField(max_length=10, verbose_name="Документы проекта")
    status_building = models.CharField(max_length=15, verbose_name="Статус строительства")
    # status = models.BooleanField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="", default="images/1.jpg", blank=True, editable=True, verbose_name="Фото")

    class Meta:
        managed = False
        db_table = 'building'

class Checking(models.Model):
    STATUS_CHOICES = (
        (1, 'Создана'),
        (2, 'На модерации'),
        (3, 'Опубликована'),
        (4, 'Закрыта'),
        (5, 'Удалёна'),
    )

    checking_id = models.BigAutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=127, verbose_name="Имя")
    age = models.IntegerField(verbose_name="Возраст")
    # status = models.CharField(max_length=15)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")

    # creation_time = models.DateField(verbose_name="Дата создания")
    # approving_date = models.DateField(verbose_name="Дата утверждения")
    # publication_date = models.DateField(verbose_name="Дата публикации")

    creation_time = models.DateTimeField(default=timezone.now)
    approving_date = models.DateTimeField(null=True, blank=True)
    publication_date = models.DateTimeField(null=True, blank=True)

    buildings = models.ManyToManyField(Building, through='CheckingsBuildings', verbose_name="Строения")
    # buildings = models.ManyToManyField(Building, related_name='checkings', blank=True)
    users = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='user_id',  # Имя поля в базе данных
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    moderator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='moderator',  # Имя поля в базе данных
        related_name='moderator_user_id',
        null=True,
        blank=True,
        verbose_name="Модератор"
    )
    # Добавить поле, фактический статус стройки здания в %
    class Meta:
        managed = False
        db_table = 'checking'


class CheckingsBuildings(models.Model):
    building_id = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='building_id',  # Имя поля в базе данных
        blank=True,
        # null=True,
        primary_key=True,
        # unique=True
    )
    # id_s = models.BigAutoField(primary_key=True, serialize=False)
    checking_id = models.ForeignKey(
        Checking,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='checking_id',  # Имя поля в базе данных
        blank=True,
        # null=True,
        # primary_key=True,
        # unique=True
    )
    class Meta:
        managed = False
        db_table = 'checkingsbuildings'
        # unique_together = ('building_id', 'checking_id')
