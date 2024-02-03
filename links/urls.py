from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('li/<str:short>', views.redirect, name='redirect'),
]