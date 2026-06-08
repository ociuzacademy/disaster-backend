from rest_framework import serializers
from .models import Resources, UserReg, VolunteerCamp, VolunteerCollectionCentre


class  UserRegRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReg
        fields = ['id', 'name', 'email', 'password', 'address', 'location', 'image', 'phone_number', 'utype']
        extra_kwargs = {
            'password': {'write_only': True}  # Prevents password from being exposed
        }



class VolunteerCampRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerCamp
        fields = ['id', 'email', 'password', 'assigned_camp', 'name', 'address', 'aadhaar', 'camp_select', 'skills_exp', 'status', 'utype']
        extra_kwargs = {
            'password': {'write_only': True}
        }





class  VolunteerCollectionCentreRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerCollectionCentre
        fields = ['id', 'email', 'password', 'assigned_collection_center', 'name', 'address', 'aadhaar', 'collection_center_select', 'skills_exp', 'status', 'utype']
        extra_kwargs = {
            'password': {'write_only': True}
        }



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserRegProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReg
        fields = ['id', 'name', 'email', 'address', 'location', 'image', 'phone_number', 'utype']
        read_only_fields = ['email', 'utype']  # Prevent modification of email and user type


class VolunteerCampProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerCamp
        fields = ['id', 'email', 'name', 'address', 'aadhaar', 'camp_select', 'skills_exp', 'status', 'utype']
        read_only_fields = ['email', 'utype', 'status']  # Prevent modification of read-only fields


class VolunteerCollectionCentreProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerCollectionCentre
        fields = ['id', 'email', 'name', 'address', 'aadhaar', 'collection_center_select', 'skills_exp', 'status', 'utype']
        read_only_fields = ['email', 'utype', 'status']  # Prevent modification of read-only fields


class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ['id', 'collectioncenter', 'name', 'description', 'quantity', 'date_recieved']
        read_only_fields = ['id', 'date_recieved']  # Prevent modification of these fields
        
        
from rest_framework import serializers
from .models import Camp, CollectionCenter, DisNews

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = ['id', 'name', 'district', 'address', 'gmap_link', 'latitude', 'longitude', 'capacity', 
                  'contact_person', 'contact_phone', 'contact_email', 'description', 'profile_pic']
        # You can add 'read_only_fields' if some fields shouldn't be edited

class CollectionCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionCenter
        fields = ['id', 'name', 'district', 'address', 'gmap_link', 'latitude', 'longitude', 'contact_person', 
                  'contact_phone', 'contact_email', 'description', 'profile_pic']

class DisNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisNews
        fields = ['id', 'title', 'description', 'news_pic', 'created_at', 'updated_at']


