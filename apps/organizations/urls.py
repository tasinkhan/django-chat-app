# urls.py
from django.urls import path
from .views import OrganizationBulkCreateAPIView

urlpatterns = [
    path('create/', OrganizationBulkCreateAPIView.as_view(), name='organization-create'),
    # path('role/create/', RoleBulkCreateAPIView.as_view(), name='role-create'),
    # path('user/create/', UserBulkCreateAPIView.as_view(), name='user-create'),
]