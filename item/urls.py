from django.contrib import admin
from django.urls import path
from item import views


urlpatterns = [
    path('', views.ItemView.as_view()),
]
