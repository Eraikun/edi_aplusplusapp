import json
from ast import If

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import RequestContext

from .forms import NameForm
from .models import Employee, Team, TeamLeader, TeamMember, WorkArrangement
from .serializers import (EmployeeSerializer, TeamSerializer, TLSerializer,
                          TMSerializer, WASerializer)

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

# a simple function which takes query employee elements and return their payment as value
def calculate_payment(_employee):
    payment = 0.0
    #we need to match employee with projects he is working on
    allProjects = WorkArrangement.objects.filter(workedOnBy=_employee.id)
    for project in allProjects:
        payment += _employee.hourlyRate * project.workDuration * 4
    #teamleader gets 10% bonus on top
    if TeamLeader.objects.filter(leader=_employee.id).exists():
        payment+= payment * 0.1
    return payment

@api_view(['GET'])
def list_employees(request):
    employees=[]
    queryset = Employee.objects.all()
    for employee in queryset:
        employees.append({"name":employee.name, "monthly_payment":calculate_payment(employee)})
    searchTerm = request.GET.get('searchEmployee')
    return render(request, 'list_employees.html',{'employees': employees})

@api_view(['POST'])
def list_employee(request):
    employees=[]
    jsonResponse = '{}'
    # create JSON data to send as result with employee name and payment
    try:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #get the form data
            searchTerm = form.cleaned_data["searchTerm"]
            try:
                #search for the employee in the database
                queryset = Employee.objects.get(name=searchTerm)
                employee={"name":queryset.name, "monthly_payment":calculate_payment(queryset)}
                return render(request, 'list_employees.html',{'employees': [employee]})
            #if nothing found we could search for search term contains
            except Employee.DoesNotExist:
                queryset = Employee.objects.filter(name__contains=searchTerm)
                for employee in queryset:
                    #add every fitting query into the json response
                    employees.append({"name":employee.name, "monthly_payment":calculate_payment(employee)})
                print(employees,"lol")
                return render(request, 'list_employees.html',{'employees': employees})
            
    except Employee.DoesNotExist:
        # there is no employee object with that given Name return proper error message
        return Response({'errors': 'Employee not found under the given Name.'}, status=400)
    

@api_view(['GET'])
def view_employees(request):
    # create JSON data to send as result with employee name and payment
    jsonResponse = '{}'
    # checking for the parameters from the URL
    if request.query_params:
        try:
            queryset = Employee.objects.get(name=request.query_params.get("name"))
            # python object to be appended to our response json
            _temp1 = {queryset.name:calculate_payment(queryset)}
            # we parse our json response
            parsedJson = json.loads(jsonResponse)
            parsedJson.update(_temp1)
            jsonResponse = json.dumps(parsedJson)
        except Employee.DoesNotExist:
            # there is no employee object with that given Name return proper error message
            return Response({'errors': 'Employee not found under the given Name.'}, status=400)
        # Serialize Employee item from Django queryset object to JSON formatted data
        read_serializer = EmployeeSerializer(queryset)
    else:
        queryset = Employee.objects.all()
        for employee in queryset:
            # calculate all work hours 
            calculate_payment(employee)
            # python object to be appended to our response json
            _temp1 = {employee.name:calculate_payment(employee)}
            # we parse our json response
            parsedJson = json.loads(jsonResponse)
            parsedJson.update(_temp1)
            jsonResponse = json.dumps(parsedJson)
        # Serialize list of Employees item from Django queryset object to JSON formatted data
        read_serializer = EmployeeSerializer(queryset, many=True)
    # if there is something in items else raise error
    if read_serializer.data:
        return Response(json.loads(jsonResponse))
    else:
        return Response(read_serializer.errors, status=400)

@api_view(['POST'])
def add_employee(request):
    employee_serializer = EmployeeSerializer(data=request.data)
    # validate user POST data
    if employee_serializer.is_valid():
        # If user data is valid, create a new Employee item record in the database
        Employee_item_object = employee_serializer.create(employee_serializer.data)
        # Serialize the new Employee item from a Python object to JSON format
        read_serializer = EmployeeSerializer(Employee_item_object)
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
    update_serializer = EmployeeSerializer(Employee_item, data=request.data)

    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        # Data was valid, update the Employee item in the database
        # and save the item for response in a variable
        Employee_item_object = update_serializer.save()
        print(Employee_item_object)
        # Serialize the Employee item from Python object to JSON format
        read_serializer = EmployeeSerializer(Employee_item_object)
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
    employee_name = EmployeeSerializer(Employee_item)
    Employee_item.delete()
    # Return a HTTP response notifying that the Employee item was successfully deleted
    return Response({'success': 'Employee {0} has been fired! :D'.format(employee_name.data.get("name"))},status=204)

# Create routes for Team 
@api_view(['GET'])
def view_team(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if Team object exists
            queryset = Team.objects.get(teamTitle=request.query_params.get("teamTitle"))
        except TeamSerializer.DoesNotExist:
            # there is no employee object with that given Name return proper error message
            return Response({'errors': 'WorkArrangement not found under the given teamTitle.'}, status=400)
        # Serialize Employee item from Django queryset object to JSON formatted data
        team_serializer = TeamSerializer(request.query_params)
    else:
        queryset = Team.objects.all()
        # Serialize list of Employees item from Django queryset object to JSON formatted data
        team_serializer = TeamSerializer(queryset, many=True)
       
    # if there is something in items else raise error
    if team_serializer.data:
        return Response(team_serializer.data)
    else:
        return Response(team_serializer.errors, status=400)
@api_view(['POST'])
def create_team(request):
    team_serializer = TeamSerializer(data=request.data)
    # validate user POST data
    if team_serializer.is_valid():
        team_item = team_serializer.create(team_serializer.data)
        # Serialize the new team item from a Python object to JSON format
        read_serializer = TeamSerializer(team_item)
        # Return a HTTP response with the newly created team item data
        return Response(read_serializer.data, status=201)
    # If the users POST data is not valid, return a 400 response with an error message
    return Response(team_serializer.errors, status=400)

@api_view(['POST'])
def update_team(request, id):
    try:
        # Check if team object exists
        team_item = Team.objects.get(id=id)
    except Team.DoesNotExist:
        # there is no team object with that given ID return proper error message
        return Response({'errors': 'Work arrangement not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = TeamSerializer(instance=team_item, data=request.data)
    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        team_item = update_serializer.save()
        # Serialize the team item from Python object to JSON format
        read_serializer = TeamSerializer(team_item)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_team(request, id):
    try:
        # Check if team item the user wants to delete exists
        team_item = Team.objects.get(id=id)
    except Team.DoesNotExist:
        # If the team item does not exist, return an error response
        return Response({'errors': 'team not found'}, status=400)
    # Delete the chosen team item from the database
    team_item_name = TeamSerializer(team_item)
    team_item.delete()
    # Return a HTTP response notifying that the team item was successfully deleted
    return Response({'success': 'Team {0} has been deleted'.format(team_item_name.data.get("teamTitle"))},status=204)

# Create routes for team member
@api_view(['GET'])
def view_member(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if team member object exists
            queryset = TeamMember.objects.get(member=request.query_params.get("member"))
        except TeamMember.DoesNotExist:
            # there is no work assignment object with that given Name return proper error message
            return Response({'errors': 'Team member not found under the given name.'}, status=400)
        # Serialize work assignment item from Django queryset object to JSON formatted data
        tm_serializer = TMSerializer(request.query_params)
        
    else:
        queryset = TeamMember.objects.all()
        # Serialize list of work assignment item from Django queryset object to JSON formatted data
        tm_serializer = TMSerializer(queryset, many=True)
       
    # if there is something in items else raise error
    if tm_serializer.data:
        return Response(tm_serializer.data)
    else:
        return Response(tm_serializer.errors, status=400)

@api_view(['POST'])
def create_member(request):
    #tm_serializer = TMSerializer(data=request.data)
    tm_serializer = TMSerializer(data={'team': Team.objects.get(teamTitle=request.data.get("team", "")).id, 'member': Employee.objects.get(name=request.data.get("employee", "")).id})
    # validate user POST data
    if tm_serializer.is_valid():
        # If user data is valid, create a new WorkArrangement item record in the database
        tm_item_object = tm_serializer.create({'team': Team.objects.get(teamTitle=request.data.get("team", "")), 'member': Employee.objects.get(name=request.data.get("employee", ""))})
        # Serialize the team member item from a Python object to JSON format
        read_serializer = TMSerializer(tm_item_object)
        # Return a HTTP response with the newly created team member item data
        return Response(read_serializer.data, status=201)
    # If the users POST data is not valid, return a 400 response with an error message
    return Response(tm_serializer.errors, status=400)

@api_view(['POST'])
def update_member(request, id):
    try:
        # Check if work assignment object exists
        tm_item = TeamMember.objects.get(id=id)
    except TeamMember.DoesNotExist:
        # there is no team member object with that given ID return proper error message
        return Response({'errors': 'Team member not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = WASerializer(instance=tm_item, data=request.data)
    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        tm_item_object = update_serializer.save()
        # Serialize the work assignment item from Python object to JSON format
        read_serializer = WASerializer(tm_item_object)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_member(request, id):
    try:
        # Check if the team member item the user wants to update exists
        tm_item = TeamMember.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # If the work assignment item does not exist, return an error response
        return Response({'errors': 'team member not found'}, status=400)
    # Delete the chosen team member  item from the database
    tm_item_name = TMSerializer(tm_item)
    tm_item.delete()
    # Return a HTTP response notifying that the team member item was successfully deleted
    return Response({'success': 'team member {0} has been deleted'.format(tm_item_name.data.get("member"))},status=204)

# Create routes for team leader
@api_view(['GET'])
def view_leader(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if team leader object exists
            queryset = TeamLeader.objects.get(leader=request.query_params.get("leader"))
        except TeamLeader.DoesNotExist:
            # there is no work assignment object with that given Name return proper error message
            return Response({'errors': 'Team leader not found under the given name.'}, status=400)
        # Serialize work assignment item from Django queryset object to JSON formatted data
        tm_serializer = TLSerializer(request.query_params)
        
    else:
        queryset = TeamLeader.objects.all()
        # Serialize list of work assignment item from Django queryset object to JSON formatted data
        tm_serializer = TLSerializer(queryset, many=True)
       
    # if there is something in items else raise error
    if tm_serializer.data:
        return Response(tm_serializer.data)
    else:
        return Response(tm_serializer.errors, status=400)

@api_view(['POST'])
def create_leader(request):
    tl_serializer = TLSerializer(data={'team': Team.objects.get(teamTitle=request.data.get("team", "")).id, 'leader': Employee.objects.get(name=request.data.get("employee", "")).id})
    # validate user POST data
    if tl_serializer.is_valid():
        # If user data is valid, create a new WorkArrangement item record in the database
        tl_item_object = tl_serializer.create({'team': Team.objects.get(teamTitle=request.data.get("team", "")), 'leader': Employee.objects.get(name=request.data.get("employee", ""))})
        # Serialize the team leader item from a Python object to JSON format
        read_serializer = TLSerializer(tl_item_object)
        # Return a HTTP response with the newly created team leader item data
        return Response(read_serializer.data, status=201)
    # If the users POST data is not valid, return a 400 response with an error message
    return Response(tl_serializer.errors, status=400)

@api_view(['POST'])
def update_leader(request, id):
    try:
        # Check if work assignment object exists
        tm_item = TeamLeader.objects.get(id=id)
    except TeamLeader.DoesNotExist:
        # there is no team leader object with that given ID return proper error message
        return Response({'errors': 'Team leader not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = WASerializer(instance=tm_item, data=request.data)
    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        tm_item_object = update_serializer.save()
        # Serialize the work assignment item from Python object to JSON format
        read_serializer = WASerializer(tm_item_object)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_leader(request, id):
    try:
        # Check if the team leader item the user wants to update exists
        tm_item = TeamLeader.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # If the work assignment item does not exist, return an error response
        return Response({'errors': 'team leader not found'}, status=400)
    # Delete the chosen team leader  item from the database
    tm_item_name = TLSerializer(tm_item)
    tm_item.delete()
    # Return a HTTP response notifying that the team leader item was successfully deleted
    return Response({'success': 'team leader {0} has been deleted'.format(tm_item_name.data.get("leader"))},status=204)



# Create routes for work assignments
@api_view(['GET'])
def view_was(request):
    # checking for the parameters from the URL
    if request.query_params:
        try:
            # Check if work assignment object exists
            queryset = WorkArrangement.objects.get(workTitle=request.query_params.get("workTitle"))
        except WorkArrangement.DoesNotExist:
            # there is no work assignment object with that given Name return proper error message
            return Response({'errors': 'WorkArrangement not found under the given workTitle.'}, status=400)
        # Serialize work assignment item from Django queryset object to JSON formatted data
        wa_serializer = WASerializer(request.query_params)
        
    else:
        queryset = WorkArrangement.objects.all()
        # Serialize list of work assignment item from Django queryset object to JSON formatted data
        wa_serializer = WASerializer(queryset, many=True)
       
    # if there is something in items else raise error
    if wa_serializer.data:
        return Response(wa_serializer.data)
    else:
        return Response(wa_serializer.errors, status=400)

@api_view(['POST'])
def create_wa(request):
    wa_serializer = WASerializer(data=request.data)
    # validate user POST data
    if wa_serializer.is_valid():
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
        # Check if work assignment object exists
        wa_item = WorkArrangement.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # there is no work assignment object with that given ID return proper error message
        return Response({'errors': 'Work arrangement not found'}, status=400)
    # Pass JSON data from user PUT request to serializer for validation
    update_serializer = WASerializer(instance=wa_item, data=request.data)
    # If data exists and is valid, proceed to save it into the database
    if update_serializer.is_valid():
        wa_item_object = update_serializer.save()
        # Serialize the work assignment item from Python object to JSON format
        read_serializer = WASerializer(wa_item_object)
        # Return a HTTP response with the newly updated Employee item
        return Response(read_serializer.data, status=200)
    else:
        return Response(update_serializer.errors, status=400)

@api_view(['DELETE'])
def delete_wa(request, id):
    try:
        # Check if the work assignment item the user wants to update exists
        wa_item = WorkArrangement.objects.get(id=id)
    except WorkArrangement.DoesNotExist:
        # If the work assignment item does not exist, return an error response
        return Response({'errors': 'work arrangement not found'}, status=400)
    # Delete the chosen work assignment item from the database
    wa_item_name = WASerializer(wa_item)
    wa_item.delete()
    # Return a HTTP response notifying that the work assignment item was successfully deleted
    return Response({'success': 'work assignment {0} has been deleted'.format(wa_item_name.data.get("workTitle"))},status=204)
