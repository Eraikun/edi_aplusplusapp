from enum import unique
from django.db import models

# Create your models here.

class Team(models.Model):
    """Represents a Team."""
    # Fields
    id = models.AutoField(
            primary_key=True
    )
    teamTitle = models.CharField(max_length=255, unique=True, null=False)
    class Meta:
        db_table = "team"

class Employee(models.Model):
    """Represents an employee who can work in multiple teams."""
    #id = models.AutoField(
    #        primary_key=True
    #    )
    # Fields
    name = models.CharField(max_length=255, null=False, unique=True)
    teamAffiliation = models.OneToOneField(Team, on_delete=models.CASCADE, default=0,related_name='belongsTo')
    hourlyRate = models.FloatField(null=False)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "employee"

    
class TeamLeader(models.Model):
    """Represents a TeamLeader."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    leader = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='name', related_name='leader')
    #A Team can only have one Leader
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    class Meta:
        db_table = "teamLeader"

class TeamMember(models.Model):
    """Represents a TeamEmployee."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    # 1:1 relation: one employee can be part of many teams
    member = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='name', related_name='member')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # is employee works full time on this work assignment? 
    class Meta:
        db_table = "teamMember"

class WorkArrangement(models.Model):
    """Represents a Work Assignment which then worked by 1 team."""
    # Fields
    #id = models.AutoField(
    #        primary_key=True
    #    )
    
    #We could make a composite key which would consist of employee and workTitle together
    # working employee
    # work duration
    WA_CHOICES = [
    ('FT', 'Full Time'),
    ('PT', 'Part Time 100%'),
    ('PT75', 'Part Time 75%'),
    ('PT50', 'Part Time 50%'),
    ('PT25', 'Part Time 25%'),
   ]
    workTitle = models.CharField(max_length=255, null=False)
    workedTime = models.CharField(max_length=255, default='Full Time',choices=WA_CHOICES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')

    class Meta:
        db_table = "workArrangement"

