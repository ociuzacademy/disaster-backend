from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Camp, CollectionCenter
from django.contrib.auth.decorators import login_required
from dis_app.models import *

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)  # Log the superuser in
                return redirect('admin_home')  # Redirect superuser to 'index.html' after successful login
            else:
                messages.error(request, "Only administrators can log in.")
        else:
            messages.error(request, "Invalid username or password.")

    # Render the login page regardless of authentication state
    return render(request, 'adminlogin.html')

# Admin home view
def admin_home(request):
    return render(request, 'index.html')

# CAMP VIEWS

def create_camp(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        district = request.POST.get('district')
        address = request.POST.get('address')
        gmap_link = request.POST.get('gmap_link')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        capacity = request.POST.get('capacity')
        contact_person = request.POST.get('contact_person')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        description = request.POST.get('description')
        profile_pic = request.FILES.get('profile_pic')

        # Create a new camp
        Camp.objects.create(
            name=name,
            district=district,
            address=address,
            gmap_link=gmap_link,
            latitude=float(latitude),
            longitude=float(longitude),
            capacity=capacity,
            contact_person=contact_person,
            contact_phone=contact_phone,
            contact_email=contact_email,
            description=description,
            profile_pic=profile_pic
        )
        
        return render(request, 'create_camp.html', {'success': True})

    return render(request, 'create_camp.html')

def camp_list(request):
    camps = Camp.objects.all()
    return render(request, 'camp_list.html', {'camps': camps})

# Update Camp View
def update_camp(request, pk):
    camp = get_object_or_404(Camp, pk=pk)

    if request.method == 'POST':
        camp.name = request.POST.get('name')
        camp.location = request.POST.get('location')
        camp.date = request.POST.get('date')  # Adjust according to your Camp model
        camp.time = request.POST.get('time')  # Adjust according to your Camp model
        camp.description = request.POST.get('description')

        # Update profile picture if a new one is uploaded
        if request.FILES.get('profile_pic'):
            camp.profile_pic = request.FILES.get('profile_pic')

        camp.save()
        return render(request, 'update_camp.html', {'success': True,'camp': camp})

    return render(request, 'update_camp.html', {'camp': camp})

# Delete Camp View
def delete_camp(request, pk):
    camp = get_object_or_404(Camp, pk=pk)
    camp.delete()
    messages.success(request, 'Camp deleted successfully!')
    return redirect('camp_list')  # Redirect to the camp list
# COLLECTION CENTER VIEWS

def create_collection_center(request):
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        district = request.POST.get('district')
        address = request.POST.get('address')
        gmap_link = request.POST.get('gmap_link')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contact_person = request.POST.get('contact_person')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        description = request.POST.get('description')
        profile_pic = request.FILES.get('profile_pic')

        # Create a new collection center
        CollectionCenter.objects.create(
            name=name,
            district=district,
            address=address,
            gmap_link=gmap_link,
            latitude=latitude,
            longitude=longitude,
            contact_person=contact_person,
            contact_phone=contact_phone,
            contact_email=contact_email,
            description=description,
            profile_pic=profile_pic
        )

        return render(request, 'create_collection_centre.html', {'success': True})

    return render(request, 'create_collection_centre.html')

def collection_center_list(request):
    collection_centers = CollectionCenter.objects.all()
    return render(request, 'collection_centre_list.html', {'collection_centers': collection_centers})

def update_collection_center(request, pk):
    collection_center = get_object_or_404(CollectionCenter, pk=pk)

    if request.method == 'POST':
        collection_center.name = request.POST.get('name')
        collection_center.district = request.POST.get('district')
        collection_center.address = request.POST.get('address')
        collection_center.gmap_link = request.POST.get('gmap_link')
        collection_center.latitude = request.POST.get('latitude')
        collection_center.longitude = request.POST.get('longitude')
        collection_center.contact_person = request.POST.get('contact_person')
        collection_center.contact_phone = request.POST.get('contact_phone')
        collection_center.contact_email = request.POST.get('contact_email')
        collection_center.description = request.POST.get('description')

        # Update profile picture if a new one is uploaded
        if request.FILES.get('profile_pic'):
            collection_center.profile_pic = request.FILES.get('profile_pic')

        collection_center.save()
        return render(request, 'update_center.html', {'success': True,'collection_center': collection_center})

    return render(request, 'update_center.html', {'collection_center': collection_center})

from django.shortcuts import get_object_or_404, render
from .models import CollectionCenter

def delete_collection_center(request, pk):
    center = get_object_or_404(CollectionCenter, pk=pk)
    center.delete()
    messages.success(request, 'Collection Center deleted successfully!')
    return redirect('collection_center_list')



from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import DisNews

# Create News View
def create_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        news_pic = request.FILES.get('news_pic')

        news_item = DisNews(
            title=title,
            description=description,
            news_pic=news_pic
        )
        news_item.save()
        messages.success(request, 'News item created successfully!')
        return render(request, 'create_news.html', {'success': True})  # Pass success flag

    return render(request, 'create_news.html')  # Render the form template for creating news

# News List View
def news_list(request):
    # Retrieve all news items from the database
    news_items = DisNews.objects.all()

    # Render the news list template with the news items
    return render(request, 'news_list.html', {'news_items': news_items})

# Update News View
def update_news(request, pk):
    news_item = get_object_or_404(DisNews, pk=pk)

    if request.method == 'POST':
        news_item.title = request.POST.get('title')
        news_item.description = request.POST.get('description')

        # Update news picture if a new one is uploaded
        if request.FILES.get('news_pic'):
            news_item.news_pic = request.FILES.get('news_pic')

        news_item.save()
        messages.success(request, 'News item updated successfully!')
        return render(request, 'update_news.html', {'news_item': news_item, 'success': True})  # Pass success flag

    return render(request, 'update_news.html', {'news_item': news_item})

# Delete News View
def delete_news(request, pk):
    news_item = get_object_or_404(DisNews, pk=pk)
    news_item.delete()
    messages.success(request, 'News item deleted successfully!')
    return redirect('news_list')  # Redirect to the news list



# View Pending Camp Volunteers' Requests
@login_required
def view_camp_volunteer_requests(request):
    """
    Display a list of volunteers who have requested to join a camp.
    Only shows volunteers with a 'pending' status.
    """
    pending_volunteers = VolunteerCamp.objects.filter(status='pending')
    return render(request, 'view_camp_volunteer_requests.html', {'volunteers': pending_volunteers})


# View Approved Camp Volunteers
@login_required
def view_approved_camp_volunteers(request):
    """
    Display a list of approved camp volunteers.
    """
    approved_volunteers = VolunteerCamp.objects.filter(status='approved')
    return render(request, 'view_approved_camp_volunteers.html', {'volunteers': approved_volunteers})


# Approve or Reject a Camp Volunteer
@login_required
def approve_reject_camp_volunteer(request, volunteer_id, action):
    """
    Approve or reject a camp volunteer.
    'action' can be 'approve' or 'reject'.
    """
    volunteer = get_object_or_404(VolunteerCamp, id=volunteer_id)
    
    if action == 'approve':
        volunteer.status = 'approved'
    elif action == 'reject':
        volunteer.status = 'rejected'
    
    volunteer.save()
    return redirect('view_camp_volunteer_requests')  # Redirect to the list after processing


# View Pending Collection Center Volunteers' Requests
@login_required
def view_collection_center_volunteer_requests(request):
    """
    Display a list of volunteers who have requested to join a collection center.
    Only shows volunteers with a 'pending' status.
    """
    pending_volunteers = VolunteerCollectionCentre.objects.filter(status='pending')
    return render(request, 'view_collection_center_volunteer_requests.html', {'volunteers': pending_volunteers})


# View Approved Collection Center Volunteers
@login_required
def view_approved_collection_center_volunteers(request):
    """
    Display a list of approved collection center volunteers.
    """
    approved_volunteers = VolunteerCollectionCentre.objects.filter(status='approved')
    return render(request, 'view_approved_collection_center_volunteers.html', {'volunteers': approved_volunteers})


# Approve or Reject a Collection Center Volunteer
@login_required
def approve_reject_collection_center_volunteer(request, volunteer_id, action):
    """
    Approve or reject a collection center volunteer.
    'action' can be 'approve' or 'reject'.
    """
    volunteer = get_object_or_404(VolunteerCollectionCentre, id=volunteer_id)
    if action == 'approve':
        volunteer.status = 'approved'
    elif action == 'reject':
        volunteer.status = 'rejected'
    volunteer.save()
    return redirect('view_collection_center_volunteer_requests')  # Redirect to the list after processing

