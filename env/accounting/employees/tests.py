from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your tests here.
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Employee, Team, TeamLeader, TeamMember, WorkArrangement
from .serializers import (EmployeeSerializer, TeamSerializer, TLSerializer,
                          TMSerializer, WASerializer)

class AddEmployeeTestCase(APITestCase):
    # Using the standard RequestFactory API to create a form POST request
    def setUp(self):
        self.employee = User.objects.create_user(username="erai", password="verybadpassword")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    def test_employee_get(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_employee_post(self):
        response = self.client.post('/api/teamleader/', {'name': 'Ömer', 'teamAffiliation': 1, 'hourlyRate':30.0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #self.detail_url: str = "factory:jobs-detail"

    #self.resource = Resource.objects.create(**self.resource_data)

    #self.job_data = {
    #    "resource": self.resource,
    #    "required_resource": 20,
    #}

    #def test_create(self) -> None:
    #    response: Response = self.client.post(
    #        self.list_url, data=self.job_data
    #    )
    #    print(response.data)
    #    self.assertEqual(response.status_code, 201)
