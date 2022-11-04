
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, WorkArrangement
from .serializers import AplusplusSerializer, WASerializer
import re, json


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all employees': 'api/employees/',
        'Search by employee': 'api/employees/?Name=employee_name',
        'Search by work title': 'api/employees/?workTitle=work_title',
        'Add employee': 'api/create',
        'Add work title': 'api/create_wa',
        'Update employee': 'api/update_employee/pk',
        'Delete employee': 'api/employee/item/pk/delete'
    }
  
    return Response(api_urls)

@api_view(['GET'])
def view_employees(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if Employee object exists
            queryset = Employee.objects.get(name=request.query_params.get("name"))
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
    if read_serializer.data:
        return Response(read_serializer.data)
    else:
        return Response(read_serializer.errors, status=400)

@api_view(['POST'])
def add_employee(request):
    employee_serializer = AplusplusSerializer(data=request.data)
    # validate user POST data
    if employee_serializer.is_valid():
        # validating for already existing data
        if Employee.objects.filter(name=request.data['name']).exists():
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
    return Response(employee_serializer.errors, status=400)

@api_view(['POST'])
def update_employee(request, id):
    try:
        # Check if Employee object exists
        Employee_item = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        # there is no employee object with that given ID return proper error message
        return Response({'errors': 'Employee not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = AplusplusSerializer(Employee_item, data=request.data)

    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        # Data was valid, update the Employee item in the database
        # and save the item for response in a variable
        Employee_item_object = update_serializer.save()
        print(Employee_item_object)
        # Serialize the Employee item from Python object to JSON format
        read_serializer = AplusplusSerializer(Employee_item_object)
        print(read_serializer)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_employee(request, id):
    try:
        # Check if the Employee item the user wants to update exists
        Employee_item = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        # If the Employee item does not exist, return an error response
        return Response({'errors': 'Employee not found'}, status=400)
    # Delete the chosen Employee item from the database
    employee_name = AplusplusSerializer(Employee_item)
    Employee_item.delete()
    # Return a HTTP response notifying that the Employee item was successfully deleted
    return Response({'success': 'Employee {0} has been fired! :D'.format(employee_name.data.get("name"))},status=204)

# Create routes für work assignments
@api_view(['GET'])
def view_was(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if Employee object exists
            queryset = WorkArrangement.objects.get(workTitle=request.query_params.get("workTitle"))
            read_serializer = WASerializer(queryset)
        except WorkArrangement.DoesNotExist:
            # there is no employee object with that given Name return proper error message
            return Response({'errors': 'WorkArrangement not found under the given workTitle.'}, status=400)
        # items = Employee.objects.filter(**request.query_param.dict())
        # Serialize Employee item from Django queryset object to JSON formatted data
        wa_serializer = WASerializer(request.query_params)
        
    else:
        queryset = WorkArrangement.objects.all()
        # Serialize list of Employees item from Django queryset object to JSON formatted data
        read_serializer = WASerializer(queryset, many=True)
       
    # if there is something in items else raise error
    if read_serializer.data:
        return Response(read_serializer.data)
    else:
        return Response(wa_serializer.errors, status=400)

@api_view(['POST'])
def create_wa(request):
    wa_serializer = WASerializer(data=request.data)
    # validate user POST data
    if wa_serializer.is_valid():
        # validating for already existing data
        #if WorkArrangement.objects.filter(workTitle=request.data['workTitle']).exists():
        #if WorkArrangement.objects.filter(**request.data).exists():
            # To-Do: Check if Name exists - can a madman be full-time and half-time WorkArrangement ._.
            #return Response({'errors': 'WorkArrangement under the given game already exists.'}, status=400)
        # If user data is valid, create a new WorkArrangement item record in the database
        wa_item_object = wa_serializer.create(wa_serializer.data)
        # Serialize the new Employee item from a Python object to JSON format
        read_serializer = WASerializer(wa_item_object)
        # Return a HTTP response with the newly created Employee item data
        return Response(read_serializer.data, status=201)
    # If the users POST data is not valid, return a 400 response with an error message
    return Response(wa_serializer.errors, status=400)

@api_view(['POST'])
def update_wa(request, id):
    try:
        # Check if Employee object exists
        wa_item = WorkArrangement.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # there is no employee object with that given ID return proper error message
        return Response({'errors': 'Work arrangement not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = WASerializer(instance=wa_item, data=request.data)
    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        wa_item_object = update_serializer.save()# Serialize the Employee item from Python object to JSON format
        read_serializer = WASerializer(wa_item_object)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_wa(request, id):
    try:
        # Check if the Employee item the user wants to update exists
        wa_item = WorkArrangement.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # If the Employee item does not exist, return an error response
        return Response({'errors': 'work arrangement not found'}, status=400)
    # Delete the chosen Employee item from the database
    wa_item_name = WASerializer(wa_item)
    wa_item.delete()
    # Return a HTTP response notifying that the Employee item was successfully deleted
    return Response({'success': 'Employee {0} has been deleted'.format(wa_item_name.data.get("workTitle"))},status=204)