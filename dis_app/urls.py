from django.urls import path
from .views import (
    CampListView,
    CollectionCenterListView,
    DisNewsListView,
    UserRegRegistrationView,
    VolunteerCampRegistrationView,
    VolunteerCollectionCentreRegistrationView,
    UserRegProfileView,
    VolunteerCampProfileView,
    VolunteerCollectionCentreProfileView,
    LoginView,
  
)

urlpatterns = [
    # Registration endpoints
    path('register/user/', UserRegRegistrationView.as_view(), name='register_user'),
    path('register/volunteer-camp/', VolunteerCampRegistrationView.as_view(), name='register_volunteer_camp'),
    path('register/volunteer-collection-centre/', VolunteerCollectionCentreRegistrationView.as_view(), name='register_volunteer_collection_centre'),
    
    # Profile endpoints
    path('profile/user/', UserRegProfileView.as_view(), name='profile_user'),
    path('profile/volunteer-camp/', VolunteerCampProfileView.as_view(), name='profile_volunteer_camp'),
    path('profile/volunteer-collection-centre/', VolunteerCollectionCentreProfileView.as_view(), name='profile_volunteer_collection_centre'),
    
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('camps/', CampListView.as_view(), name='camp-list'),

    path('collection-centers/', CollectionCenterListView.as_view(), name='collection-center-list'),
    path('news/', DisNewsListView.as_view(), name='disnews-list'),
]
