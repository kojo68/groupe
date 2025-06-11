
from django.urls import path
from .views import acheter

urlpatterns = [
    path('', acheter, name='acheter'),
]
