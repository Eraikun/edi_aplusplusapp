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
    team = serializers.SlugRelatedField(slug_field='teamTitle', read_only="True")
    member = serializers.SlugRelatedField(slug_field='name', read_only="True")
    class Meta:
        model = TeamMember
        fields = ('id', 'team', 'member')

class TLSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='teamTitle', read_only="True")
    leader = serializers.SlugRelatedField(slug_field='name', read_only="True")
    class Meta:
        model = TeamLeader
        fields = ('id', 'team', 'leader')