import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_verification(request):
    user = identity_user(request)

    if user is None:
        return None

    verification = Verification.objects.filter(owner_id=user.id).filter(status=1).first()

    return verification


@api_view(["GET"])
def search_buildings(request):
    query = request.GET.get("query", "")

    building = Building.objects.filter(status=1).filter(name__icontains=query)

    serializer = BuildingSerializer(building, many=True)

    draft_verification = get_draft_verification(request)

    resp = {
        "buildings": serializer.data,
        "draft_verification_id": draft_verification.pk if draft_verification else None
    }

    return Response(resp)


@api_view(["GET"])
def get_building_by_id(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    serializer = BuildingSerializer(building, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_building(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    serializer = BuildingSerializer(building, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_building(request):
    building = Building.objects.create()

    serializer = BuildingSerializer(building)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_building(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    building.status = 2
    building.save()

    building = Building.objects.filter(status=1)
    serializer = BuildingSerializer(building, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_building_to_verification(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)

    draft_verification = get_draft_verification(request)

    if draft_verification is None:
        draft_verification = Verification.objects.create()
        draft_verification.owner = identity_user(request)
        draft_verification.save()

    if BuildingVerification.objects.filter(verification=draft_verification, building=building).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = BuildingVerification.objects.create()
    item.verification = draft_verification
    item.building = building
    item.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_building_image(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)

    return HttpResponse(building.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_building_image(request, building_id):
    if not Building.objects.filter(pk=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    building = Building.objects.get(pk=building_id)
    serializer = BuildingSerializer(building, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_verifications(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    verifications = Verification.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        verifications = verifications.filter(owner=user)

    if status_id != -1:
        verifications = verifications.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        verifications = verifications.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        verifications = verifications.filter(date_formation__lt=parse_datetime(date_end))

    serializer = VerificationsSerializer(verifications, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_verification_by_id(request, verification_id):
    if not Verification.objects.filter(pk=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    verification = Verification.objects.get(pk=verification_id)
    serializer = VerificationSerializer(verification, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_verification(request, verification_id):
    if not Verification.objects.filter(pk=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    verification = Verification.objects.get(pk=verification_id)
    serializer = VerificationSerializer(verification, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, verification_id):
    if not Verification.objects.filter(pk=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    verification = Verification.objects.get(pk=verification_id)

    verification.status = 2
    verification.date_formation = timezone.now()
    verification.save()

    items = BuildingVerification.objects.filter(verification=verification)
    for item in items:
        calculate_building_state(verification_id, item.building.pk)

    serializer = VerificationSerializer(verification, many=False)

    return Response(serializer.data)


def calculate_building_state(verification_id, building_id):
    data = {
        "verification_id": verification_id,
        "building_id": building_id
    }

    requests.post("http://127.0.0.1:8080/calc_building_state/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, verification_id):
    if not Verification.objects.filter(pk=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    verification = Verification.objects.get(pk=verification_id)

    if verification.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    verification.status = request_status
    verification.date_complete = timezone.now()
    verification.save()

    serializer = VerificationSerializer(verification, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_verification(request, verification_id):
    if not Verification.objects.filter(pk=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    verification = Verification.objects.get(pk=verification_id)

    if verification.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    verification.status = 5
    verification.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_building_from_verification(request, verification_id, building_id):
    if not BuildingVerification.objects.filter(verification_id=verification_id, building_id=building_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = BuildingVerification.objects.get(verification_id=verification_id, building_id=building_id)
    item.delete()

    if not BuildingVerification.objects.filter(verification_id=verification_id).exists():
        verification = Verification.objects.get(pk=verification_id)
        verification.delete()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_building_in_verification(request, verification_id, building_id):
    if not BuildingVerification.objects.filter(building_id=building_id, verification_id=verification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = BuildingVerification.objects.get(building_id=building_id, verification_id=verification_id)

    serializer = BuildingVerificationSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован!',
        'user_id': user.id,
        "access_token": access_token
    }

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def verification(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)
