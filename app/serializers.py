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
        fields = ('name',)


class VerificationsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Verification
        fields = "__all__"


class VerificationSerializer(serializers.ModelSerializer):
    buildings = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_buildings(self, verification):
        items = BuildingVerification.objects.filter(verification_id=verification.pk)

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