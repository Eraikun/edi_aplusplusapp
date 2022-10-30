
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import AplusplusSerializer
import re, json


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
  
    return Response(api_urls)


@api_view(['POST'])
def add_employee(request):
    employee_serializer = AplusplusSerializer(data=request.data)
    # validate user POST data
    if employee_serializer.is_valid():
        # validating for already existing data
        if Employee.objects.filter(Name=request.data['Name']).exists():
        #if Employee.objects.filter(**request.data).exists():
            # To-Do: Check if Name exists - can a madman be full-time and half-time employee ._.
            return Response({'errors': 'Employee under the given game already exists.'}, status=400)
        # If user data is valid, create a new Employee item record in the database
        Employee_item_object = employee_serializer.create(employee_serializer.data)
        # Serialize the new Employee item from a Python object to JSON format
        read_serializer = AplusplusSerializer(Employee_item_object)
        # Return a HTTP response with the newly created Employee item data
        return Response(read_serializer.data, status=201)
    # If the users POST data is not valid, return a 400 response with an error message
    return Response(status=status.HTTP_404_NOT_FOUND)
