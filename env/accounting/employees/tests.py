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


class EmployeeTestCase(TestCase):
    def setUp(self):
        print('set up some employees')
        t1 = Team.objects.create(teamTitle="winner")
        Employee.objects.create(name= 'Don', teamAffiliation= t1, hourlyRate=12.0)
        Employee.objects.create(name= 'Jan', teamAffiliation= t1, hourlyRate=19.0)
    def test_employee_list(self):
        print('testing employee information')
        qS = Employee.objects.all()
        # check if database successfully added both test employees
        self.assertEqual(qS.count(),2)
        e1 = Employee.objects.get(name = "Don")
        e2 = Employee.objects.get(name = "Jan")
        self.assertEqual(e1.get_salary(),e1.hourlyRate*8*5*4)
        self.assertEqual(e2.get_salary(),e2.hourlyRate*8*5*4)
    def test_employee_get(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #def test_employee_post(self):
    #    t1 = Team.objects.create(teamTitle="procrastinater")
    #    response = self.client.post('/api/teamleader/', {'name': 'Römer', 'teamAffiliation': t1.pk, 'hourlyRate':30.0})
    #    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
