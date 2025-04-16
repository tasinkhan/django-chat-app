from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializer


class RoleBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)
        print("===the value of many====", many)
        serializer = RoleSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the objects to be bulk created
            if many:
                # Collect the roles to be bulk created
                roles = [
                    Role(**validated_data)
                    for validated_data in serializer.validated_data
                ]
                Role.objects.bulk_create(roles)
                return Response(
                    {"detail": "roles created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                Role.objects.create(**serializer.validated_data)
                return Response(
                    {"detail": "Role created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
