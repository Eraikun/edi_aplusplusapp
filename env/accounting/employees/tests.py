from django.test import TestCase
from rest_framework import status
# Create your tests here.
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Employee, Team, TeamLeader, TeamMember, WorkArrangement
from .serializers import (EmployeeSerializer, TeamSerializer, TLSerializer,
                          TMSerializer, WASerializer)

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/api/teamleader/', {'name': 'Ömer', 'teamAffiliation': 1, 'hourlyRate':30.0})
