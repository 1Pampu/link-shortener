from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('li/<str:short>', views.redirect, name='redirect'),
    path('created/', views.created, name='created'),
]