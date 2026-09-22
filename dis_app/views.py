from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from .models import UserReg, VolunteerCamp, VolunteerCollectionCentre
from rest_framework.permissions import AllowAny
from .weather_service import (
    get_weather,
    get_current_weather,
    get_daily_forecast,
    calculate_risk,
    calculate_forecast_risk,
    calculate_overall_risk
)
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

#Weather
class WeatherPredictionView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        # -----------------------------------------
        # GET JSON DATA
        # -----------------------------------------

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if latitude is None or longitude is None:

            return Response(
                {
                    "status": False,
                    "message": (
                        "Latitude and longitude "
                        "are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CONVERT TO FLOAT
        # -----------------------------------------

        try:

            latitude = float(latitude)
            longitude = float(longitude)

        except (ValueError, TypeError):

            return Response(
                {
                    "status": False,
                    "message": (
                        "Latitude and longitude "
                        "must be valid numbers."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # LATITUDE VALIDATION
        # -----------------------------------------

        if latitude < -90 or latitude > 90:

            return Response(
                {
                    "status": False,
                    "message": (
                        "Latitude must be "
                        "between -90 and 90."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # LONGITUDE VALIDATION
        # -----------------------------------------

        if longitude < -180 or longitude > 180:

            return Response(
                {
                    "status": False,
                    "message": (
                        "Longitude must be "
                        "between -180 and 180."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # FETCH WEATHER
        # -----------------------------------------

        try:

            weather_data = get_weather(
                latitude,
                longitude
            )

            # -------------------------------------
            # CURRENT WEATHER
            # -------------------------------------

            current_weather = get_current_weather(
                weather_data
            )

            # -------------------------------------
            # CURRENT RISK
            # -------------------------------------

            current_risk = calculate_risk(
                weather_data.get(
                    "current",
                    {}
                )
            )

            # -------------------------------------
            # 7-DAY FORECAST
            # -------------------------------------

            forecast = get_daily_forecast(
                weather_data
            )

            # -------------------------------------
            # FORECAST RISK
            # -------------------------------------

            forecast_risk = calculate_forecast_risk(
                forecast
            )

            # -------------------------------------
            # OVERALL RISK
            # -------------------------------------

            overall_risk = calculate_overall_risk(
                current_risk,
                forecast_risk
            )

            # -------------------------------------
            # RESPONSE
            # -------------------------------------

            return Response(
                {
                    "status": True,

                    "message": (
                        "Weather prediction "
                        "fetched successfully."
                    ),

                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "timezone": weather_data.get(
                            "timezone"
                        )
                    },

                    "current": current_weather,

                    "risk": {
                        "current": current_risk,
                        "forecast": forecast_risk,
                        "overall": overall_risk
                    },

                    "forecast": forecast
                },

                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "status": False,
                    "message": (
                        "Unable to fetch "
                        "weather data."
                    ),
                    "error": str(e)
                },

                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )