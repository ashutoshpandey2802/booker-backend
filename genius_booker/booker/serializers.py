from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile,Store, Staff

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    store_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'store_name']

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        
        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        
        return data

    def create(self, validated_data):
        store_name = validated_data.pop('store_name')
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create or update the UserProfile
        user_profile, _ = UserProfile.objects.update_or_create(
            user=user,
            defaults={'store_name': store_name}
        )

        return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid email or password")



class StaffSerializer(serializers.ModelSerializer):
    stores = serializers.SerializerMethodField()
    
    class Meta:
        model = Staff
        fields = '__all__'
    
    def get_stores(self, obj):
        # Return store IDs or names as a list of strings or integers
        return [store.id for store in obj.stores.all()] 

class StoreSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True, read_only=True, source='staff_set')

    class Meta:
        model = Store
        fields ='__all__'
