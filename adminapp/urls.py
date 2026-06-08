from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_login, name='admin_login'),  # URL for admin-only login
    path('admin_home/', admin_home, name='admin_home'),
    path('create-camp/', create_camp, name='create_camp'),
    path('camps/', camp_list, name='camp_list'),
    path('update-camp/<int:pk>/', update_camp, name='update_camp'),
    path('delete-camp/<int:pk>/', delete_camp, name='delete_camp'),

    path('create-collection-center/', create_collection_center, name='create_collection_center'),
    path('collection_center_list/', collection_center_list, name='collection_center_list'),
    path('update-collection-center/<int:pk>/', update_collection_center, name='update_collection_center'),
    path('delete-collection-center/<int:pk>/', delete_collection_center, name='delete_collection_center'),

    # News URLs
    path('create-news/', create_news, name='create_news'),  # URL for creating news
    path('news/', news_list, name='news_list'),             # URL for listing news
    path('update-news/<int:pk>/', update_news, name='update_news'),  # URL for updating news
    path('delete-news/<int:pk>/', delete_news, name='delete_news'),  # URL for deleting news
    
      # Volunteer views for camps
    path('view_camp_volunteer_requests/', view_camp_volunteer_requests, name='view_camp_volunteer_requests'),
    path('view_approved_camp_volunteers/', view_approved_camp_volunteers, name='view_approved_camp_volunteers'),
    path('approve_reject_camp_volunteer/<int:volunteer_id>/<str:action>/', approve_reject_camp_volunteer, name='approve_reject_camp_volunteer'),

    # Volunteer views for collection centers
    path('view_collection_center_volunteer_requests/', view_collection_center_volunteer_requests, name='view_collection_center_volunteer_requests'),
    path('view_approved_collection_center_volunteers/', view_approved_collection_center_volunteers, name='view_approved_collection_center_volunteers'),
    path('approve_reject_collection_center_volunteer/<int:volunteer_id>/<str:action>/', approve_reject_collection_center_volunteer, name='approve_reject_collection_center_volunteer'),
]

