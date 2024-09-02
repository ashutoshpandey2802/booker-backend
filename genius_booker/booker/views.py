from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, RegisterSerializer,StoreSerializer, StaffSerializer
from .models import Store, Staff
from rest_framework import viewsets

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
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        stores = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "status_code": status.HTTP_201_CREATED,
            "status": "success",
            "message": "Stores created successfully",
            "stores": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        staff_members = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "status_code": status.HTTP_201_CREATED,
            "status": "success",
            "message": "Staff members created successfully",
            "staff": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)