# urls.py
from django.urls import path
from .views import RoleBulkCreateAPIView

urlpatterns = [
    path('create/', RoleBulkCreateAPIView.as_view(), name='role-create')
]
