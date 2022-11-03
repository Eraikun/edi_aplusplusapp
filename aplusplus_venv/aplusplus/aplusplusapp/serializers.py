from rest_framework import serializers
from django.db.models import fields
from .models import Employee, WorkArrangement


class AplusplusSerializer(serializers.ModelSerializer):
  # id = serializers.AutoField(primary_key=True)
  Name = serializers.CharField(max_length=255)
  Team_Affiliation = serializers.CharField(max_length=255)
  Hourly_Rate = serializers.DecimalField(max_digits=6, decimal_places=2)
  def create(self, validated_data):
    # Once the request data has been validated, we can create a todo item instance in the database
    return Employee.objects.create(
      Name=validated_data.get('Name'), Team_Affiliation=validated_data.get('Team_Affiliation'), Hourly_Rate=validated_data.get('Hourly_Rate')
    )
  class Meta:
    model = Employee
    fields = (
      'id',
      'Name',
      'Team_Affiliation',
      'Hourly_Rate'
    )

class WASerializer(serializers.ModelSerializer):
  employee = serializers.CharField(max_length=255)
  workTitle = serializers.CharField(max_length=255)
  def create(self, validated_data):
    # Once the request data has been validated, we can create a todo item instance in the database
    whichEmployee = Employee.objects.get(Name=validated_data.get('employee'))
    return WorkArrangement.objects.create(
      employee=whichEmployee, workTitle=validated_data.get('workTitle')
    )
  class Meta:
    model = WorkArrangement
    fields = (
      'id',
      'employee',
      'workTitle',
    )
  