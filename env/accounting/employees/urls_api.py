from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.add_employee, name='add-employee'),
    path('employees/', views.view_employees, name='view_employees'),
    path('update_employee/<int:id>/', views.update_employee, name='update-employee'),
    path('employee/<int:id>/delete/', views.delete_employee, name='delete-employee'),
    path('team/', views.view_team, name='view-team'),
    path('create_team/', views.create_team, name='add-team'),
    path('update_team/<int:id>/', views.update_team, name='update-team'),
    path('team/<int:id>/delete/', views.delete_team, name='delete-team'),
    path('work_arrangements/', views.view_was, name='view_wa'),
    path('create_wa/', views.create_wa, name='add-wa'),
    path('update_wa/<int:id>/', views.update_wa, name='update-wa'),
    path('work_arrangements/<int:id>/delete/', views.delete_wa, name='delete-wa'),
    path('teammember/', views.view_member, name='view-team'),
    path('create_member/', views.create_member, name='add-member'),
    path('update_member/<int:id>/', views.update_member, name='update-member'),
    path('teammember/<int:id>/delete/', views.delete_member, name='delete-member'),
    path('teamleader/', views.view_leader, name='view-leader'),
    path('create_leader/', views.create_leader, name='add-leader'),
    path('update_leader/<int:id>/', views.update_leader, name='update-leader'),
    path('teamleader/<int:id>/delete/', views.delete_leader, name='delete-leader'),
]
