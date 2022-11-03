"""aplusplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.add_employee, name='add-employee'),
    path('employees/', views.view_employees, name='view_employees'),
    path('update_employee/<int:id>/', views.update_employee, name='update-employee'),
    path('employee/<int:id>/delete/', views.delete_employee, name='delete-employee'),
    path('work_arrangements/', views.view_was, name='view_wa'),
    path('create_wa/', views.create_wa, name='add-wa'),
    path('change_wa/<int:id>/', views.update_wa, name='update-wa'),
    path('employee/<int:id>/delete/', views.delete_wa, name='delete-wa'),
]
