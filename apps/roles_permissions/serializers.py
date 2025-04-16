from rest_framework import serializers
from .models import Role, Organization
from apps.organizations.serializers import OrganizationSerializer


class RoleSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )

    class Meta:
        model = Role
        fields = ["id", "name", "organization"]
