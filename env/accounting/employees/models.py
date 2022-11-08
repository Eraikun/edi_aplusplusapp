from django.db import models
from enum import unique
# Create your models here.
class Team(models.Model):
    """Represents a Team."""
    teamTitle = models.CharField(max_length = 255, unique = True, null = False, default = "unassigned")

    def __str__(self):
        return self.teamTitle
    class Meta:
        db_table = "team"

class Employee(models.Model):
    """Represents an employee who can work in multiple teams."""
    name = models.CharField(max_length = 255, unique = True)
    teamAffiliation = models.ForeignKey(Team, on_delete = models.CASCADE)
    hourlyRate = models.FloatField()
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "employee"

class TeamLeader(models.Model):
    """Represents a TeamLeader."""
    team = models.OneToOneField(Team, on_delete = models.CASCADE)
    leader = models.ForeignKey(Employee, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.leader
    class Meta:
        db_table = "teamLeader"

class TeamMember(models.Model):
    """Represents a TeamEmployee."""
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name='team')
    member = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name='employee')

    def __str__(self):
        return self.member
    class Meta:
        db_table = "teamMember"

class WorkArrangement(models.Model):
    """Represents a Work Assignment which then worked by 1 team."""
    workTitle = models.CharField(max_length = 255)
    workedOnBy = models.ForeignKey(Employee, on_delete = models.CASCADE)
    workDuration = models.IntegerField()
    def __str__(self) -> str:
        return self.workTitle
    class Meta:
        db_table = "workArrangement"
