from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.staff_registeration, name="staff_registeration"),
    path('staff_login', views.staff_login, name="staff_login"),
    path('staff_dashboard', views.staff_dashboard, name="staff_dashboard"),
    path('staff_logout', views.logoutPage, name="staff_logout"),
    path('csv_download', views.csv_download, name="csv_download"),

]