
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

@api_view(['GET'])
def view_employees(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if Employee object exists
            queryset = Employee.objects.get(Name=request.query_params.get("Name"))
        except Employee.DoesNotExist:
            # there is no employee object with that given Name return proper error message
            return Response({'errors': 'Employee not found under the given Name.'}, status=400)
        # items = Employee.objects.filter(**request.query_param.dict())
        # Serialize Employee item from Django queryset object to JSON formatted data
        read_serializer = AplusplusSerializer(queryset)
    else:
        queryset = Employee.objects.all()
        # Serialize list of Employees item from Django queryset object to JSON formatted data
        read_serializer = AplusplusSerializer(queryset, many=True)
    # if there is something in items else raise error
    if read_serializer:
        return Response(read_serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
