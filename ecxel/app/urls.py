# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_employee, name='search_employee'),
    path('download_pdf/', views.download_employee_data_pdf, name='download_employee_pdf'),
]
