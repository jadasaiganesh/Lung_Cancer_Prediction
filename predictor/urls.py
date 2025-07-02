from django.urls import path
from .views import homepage, predict

urlpatterns = [
    path('', homepage, name='homepage'),
    path('predict/', predict, name='predict'),
]
