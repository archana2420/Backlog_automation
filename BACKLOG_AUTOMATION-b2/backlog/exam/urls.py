from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('paymentComplete', views.success, name="success"),
    path('student_info', views.student_information, name="student_info"),
    path('display', views.display_information, name="display"),
    path('handle_request/', views.handle_request, name="handle_request"),
    # path('checkout/', views.checkout, name="Checkout"),
    # path('final_details', views.final_details, name="final_details")
    # path('display', views.display_information, name="display")
    path('ajax/load-semesters/', views.load_semesters, name='load_semesters'),
    path('ajax/load_subjects/', views.load_subjects, name='load_subjects'),


    ### STAFF URLS ###
    # path('staff_login/', auth_views.LoginView.as_view(), name='staff_login'),
    # path('staff_logout/', auth_views.LogoutView.as_view(), name='staff_logout'),
]
