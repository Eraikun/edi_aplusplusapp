from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('list_employees/', views.list_employees, name='list_employees'),
    path('list_employee/', views.list_employee, name='list_employee'),
]
