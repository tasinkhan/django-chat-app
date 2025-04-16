from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import UserSerializer
from apps.core.tasks import send_bulk_email
from django.contrib.auth.hashers import make_password

class UserBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)

        # Initialize the User serializer with the data
        serializer = UserSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the users to be bulk created
            users_to_create = []
            email_queue = []
            print("1")
            if many:
                for validated_data in serializer.validated_data:
                    role = validated_data["role"]
                    organization = validated_data["organization"]
                    password = validated_data["password"]

                    # Hash the password if it's not already hashed
                    hashed_password = make_password(password)

                    # Create the User instance
                    user_instance = User(
                        username=validated_data["username"],
                        email=validated_data["email"],
                        role=role,
                        organization=organization,
                        password=hashed_password,
                    )
                    users_to_create.append(user_instance)
                    email_queue.append(
                        (validated_data["email"], validated_data["username"])
                    )

                # Bulk create the users
                User.objects.bulk_create(users_to_create)

                # Send welcome emails to all users asynchronously
                subject = "Welcome to Our Platform"
                message = "Hello, welcome to our platform. Your account has been created successfully!"
                send_bulk_email.delay(subject, message, email_queue)

                return Response(
                    {"detail": "Users created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                validated_data = serializer.validated_data
                password = validated_data.get("password")
                validated_data["password"] = make_password(password)
                User.objects.create(**validated_data)

                return Response(
                    {"detail": "User created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
