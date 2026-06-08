from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from .models import UserReg, VolunteerCamp, VolunteerCollectionCentre
from .serializers import (
    UserRegRegistrationSerializer,
    VolunteerCampRegistrationSerializer,
    VolunteerCollectionCentreRegistrationSerializer,
    UserRegProfileSerializer,
    VolunteerCampProfileSerializer,
    VolunteerCollectionCentreProfileSerializer,
)


class UserRegRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerCampRegistrationView(APIView):
    def post(self, request):
        serializer = VolunteerCampRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Volunteer Camp registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerCollectionCentreRegistrationView(APIView):
    def post(self, request):
        serializer = VolunteerCollectionCentreRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Volunteer Collection Centre registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserRegProfileSerializer(user)
        return Response(serializer.data)


class VolunteerCampProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = VolunteerCampProfileSerializer(user)
        return Response(serializer.data)


class VolunteerCollectionCentreProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = VolunteerCollectionCentreProfileSerializer(user)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        user_type = None

        # Check UserReg model
        if UserReg.objects.filter(email=email).exists():
            user = UserReg.objects.filter(email=email).first()
            user_type = "User"

        # Check VolunteerCollectionCentre model
        elif VolunteerCollectionCentre.objects.filter(email=email).exists():
            user = VolunteerCollectionCentre.objects.filter(email=email).first()
            user_type = "Volunteer Collection Centre"

        # Check VolunteerCamp model
        elif VolunteerCamp.objects.filter(email=email).exists():
            user = VolunteerCamp.objects.filter(email=email).first()
            user_type = "Volunteer Camp"

        # If no user is found
        if not user:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate password
        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Log in the user
        login(request, user)
        session_id = request.session.session_key

        return Response(
            {
                "message": f"Login successful as {user_type}",
                "session_id": session_id,
            },
            status=status.HTTP_200_OK
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Camp, CollectionCenter, DisNews
from .serializers import CampSerializer, CollectionCenterSerializer, DisNewsSerializer

# View for Camp model
class CampListView(APIView):
    def get(self, request, *args, **kwargs):
        camps = Camp.objects.all()  # Get all camps
        serializer = CampSerializer(camps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for CollectionCenter model
class CollectionCenterListView(APIView):
    def get(self, request, *args, **kwargs):
        collection_centers = CollectionCenter.objects.all()
        serializer = CollectionCenterSerializer(collection_centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for DisNews model
class DisNewsListView(APIView):
    def get(self, request, *args, **kwargs):
        news = DisNews.objects.all()
        serializer = DisNewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
