from rest_framework import serializers
from .models import Employee, Team, WorkArrangement, TeamMember, TeamLeader

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = ('__all__')

class EmployeeSerializer(serializers.ModelSerializer):
    #name = serializers.CharField()
    #teamAffiliation = TeamSerializer(read_only=True, many=True)
    #hourlyRate = serializers.FloatField()
    class Meta:
        model = Employee 
        fields = ('pk', 'name', 'teamAffiliation', 'hourlyRate')
class WASerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkArrangement
        fields = ('id', 'workTitle', 'workedOnBy', 'workDuration')

class TMSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'team', 'member')

class TLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ('id', 'team', 'leader')