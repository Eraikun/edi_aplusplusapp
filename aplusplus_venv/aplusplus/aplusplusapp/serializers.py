from rest_framework import serializers
from django.db.models import fields
from .models import Employee, WorkArrangement, Team


class AplusplusSerializer(serializers.ModelSerializer):
  # id = serializers.AutoField(primary_key=True)
  #name = serializers.CharField(max_length=255)
  #teamAffiliation = serializers.CharField(max_length=255)
  #hourlyRate = serializers.DecimalField(max_digits=6, decimal_places=2)
  def create(self, validated_data):
    # Once the request data has been validated, we can create a todo item instance in the database
    return Employee.objects.create(
      **validated_data
    )
  class Meta:
    model = Employee
    fields = ('__all__')

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = ('__all__')

class WASerializer(serializers.ModelSerializer):
  #employee = serializers.CharField(max_length=255)
  #workTitle = serializers.CharField(max_length=255)
  #employee = AplusplusSerializer(source='employee', required=False)
  def create(self, validated_data):
    # Once the request data has been validated, we can create a todo item instance in the database
    return WorkArrangement.objects.create(
      workTitle=validated_data.get('workTitle'), workedTime=validated_data.get('workedTime'), employee=Employee.objects.get(id=validated_data.get('employee'))
    )
  def update(self, instance, validated_data):
    instance.workTitle = validated_data.get('workTitle', instance.workTitle)
    instance.workedTime = validated_data.get('workedTime', instance.workedTime)
    instance.employee = validated_data.get('employee', instance.employee)
    instance.save()
    return instance
  class Meta:
    model = WorkArrangement
    fields = ['workTitle', 'workedTime' ,'employee']
  