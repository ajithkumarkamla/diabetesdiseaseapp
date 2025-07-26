"""
URL configuration for diabetespredict_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('index/', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/',views.login_view,name='login'),
    path('download_pdf/', views.generate_pdf, name='download_pdf'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('logout/', views.logout_view, name='logout'),
    path('diabetes-info/', views.diabetes_info, name='diabetes_info'),
    path('glucose-monitoring/', views.glucose_monitoring, name='glucose_monitoring'),
    path('delete-reading/<int:reading_id>/', views.delete_reading, name='delete_reading'),

]


