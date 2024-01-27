# from bmstu_lab.models import Users, Building, Checking, CheckingsBuildings
from bmstu_lab.models import *
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Building
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

class CheckingSerializer(serializers.ModelSerializer):
    buildings = BuildingSerializer(many=True)

    users = UsersSerializer()
    moderator = UsersSerializer()

    class Meta:
        # Модель, которую мы сериализуем
        model = Checking
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['users'] = instance.users.login
        representation['moderator'] = instance.moderator.login
        return representation

class CheckingsBuildingsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = CheckingsBuildings
        # Поля, которые мы сериализуем (Все поля)
        fields = '__all__'

# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ('id', 'email', 'password', 'name')
#         write_only_fields = ('password',)
#         read_only_fields = ('id',)

#     def create(self, validated_data):
#         user = Users.objects.create(
#             email=validated_data['email'],
#             name=validated_data['name']
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)