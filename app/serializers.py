from rest_framework import serializers

from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    def get_state(self, building):
        return self.context.get("state", "")

    class Meta:
        model = Building
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class VerificationsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()
    buildings_calculated = serializers.SerializerMethodField()

    def get_owner(self, order):
        return order.owner.name

    def get_moderator(self, order):
        if order.moderator:
            return order.moderator.name

        return ""

    def get_buildings_calculated(self, verification):
        items = BuildingVerification.objects.filter(verification=verification)
        return items.filter(state__gte=0).count()

    class Meta:
        model = Verification
        fields = "__all__"


class VerificationSerializer(serializers.ModelSerializer):
    buildings = serializers.SerializerMethodField()
    buildings_calculated = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, order):
        return order.owner.name

    def get_moderator(self, order):
        if order.moderator:
            return order.moderator.name

        return ""

    def get_buildings(self, verification):
        items = BuildingVerification.objects.filter(verification=verification)

        buildings = []
        for item in items:
            serializer = BuildingSerializer(
                item.building,
                context={
                    "state": item.state
                }
            )
            buildings.append(serializer.data)

        return buildings

    def get_buildings_calculated(self, verification):
        items = BuildingVerification.objects.filter(verification=verification)
        return items.filter(state__gte=0).count()

    class Meta:
        model = Verification
        fields = "__all__"


class BuildingVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingVerification
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)