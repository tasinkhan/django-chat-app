from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer

# Create your views here.


class OrganizationBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)
        print("===the value of many====", many)
        serializer = OrganizationSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the objects to be bulk created
            if many:
                # Collect the organizations to be bulk created
                organizations = [
                    Organization(**validated_data)
                    for validated_data in serializer.validated_data
                ]
                Organization.objects.bulk_create(organizations)
                return Response(
                    {"detail": "Organizations created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                Organization.objects.create(**serializer.validated_data)
                return Response(
                    {"detail": "Organization created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)