from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile,Store, Staff
from django.core.exceptions import ValidationError

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
    stores = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Staff
        fields = '__all__'

    def validate_stores(self, stores):
        
        store_ids = []
        for store in stores:
            if isinstance(store, int):
                # Handle as store ID
                if Store.objects.filter(id=store).exists():
                    store_ids.append(store)
                else:
                    raise serializers.ValidationError(f"Store with ID '{store}' does not exist.")
            elif isinstance(store, str):
                if store.isdigit():  # If the string is a number, treat it as an ID
                    store_id = int(store)
                    if Store.objects.filter(id=store_id).exists():
                        store_ids.append(store_id)
                    else:
                        raise serializers.ValidationError(f"Store with ID '{store}' does not exist.")
                else:  # Handle as store name
                    try:
                        store_obj = Store.objects.get(name=store)
                        store_ids.append(store_obj.id)
                    except Store.DoesNotExist:
                        raise serializers.ValidationError(f"Store with name '{store}' does not exist.")
            else:
                raise serializers.ValidationError(f"Invalid store identifier: {store}")

        return store_ids



class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the store name is unique.
        """
        if Store.objects.filter(name=value).exists():
            raise serializers.ValidationError("A store with this name already exists.")
        return value
