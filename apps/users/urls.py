# urls.py
from django.urls import path
from .views import UserBulkCreateAPIView

urlpatterns = [
    path('create/', UserBulkCreateAPIView.as_view(), name='user-create')
]
