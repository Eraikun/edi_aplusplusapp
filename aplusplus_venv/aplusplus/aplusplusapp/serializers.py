from rest_framework import serializers
from django.db.models import fields
from .models import Employee, WorkArrangement, Team


class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = ('__all__')

class AplusplusSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField()
  hourlyRate = serializers.IntegerField()
  teamAffiliation = TeamSerializer(read_only=True, many=True)
  #def create(self, validated_data):
  #  return Employee.objects.create(**validated_data)
  class Meta:
    model = Employee
    fields = ['id', 'name', 'hourlyRate' ,'teamAffiliation']



class WASerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)
  workTitle = serializers.CharField()
  employee = AplusplusSerializer(read_only=True, many=True, allow_null=True)
  workedTime = serializers.CharField()
  #def create(self, validated_data):
  #  return WorkArrangement.objects.create(**validated_data)
  class Meta:
    model = WorkArrangement
    fields = ['id', 'workTitle','employee','workedTime']
  