from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, RegisterSerializer,StoreSerializer, StaffSerializer
from .models import Store, Staff
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from . import serializers

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user and associated profile
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)



class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key, 
                "message": "User registered successfully"
            },
            status=status.HTTP_200_OK)


class LogoutUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Successfully logged out"
        }, status=status.HTTP_200_OK)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "status_code": status.HTTP_201_CREATED,
            "status": "success",
            "message": "Store created successfully",
            "store": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        staff_data = request.data.get('staff', [])
        store_ids_or_names = request.data.get('stores', [])

        if not store_ids_or_names:
            return Response({"stores": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        created_staff = []

        for staff_member_data in staff_data:
            staff_member_data['stores'] = store_ids_or_names
            
            serializer = self.get_serializer(data=staff_member_data)
            serializer.is_valid(raise_exception=True)
            staff_member = serializer.save()

            created_staff.append(staff_member)

        response_data = {
            "status_code": status.HTTP_201_CREATED,
            "status": "success",
            "message": "Staff member(s) created and assigned to stores successfully",
            "staff": [StaffSerializer(staff).data for staff in created_staff]
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
