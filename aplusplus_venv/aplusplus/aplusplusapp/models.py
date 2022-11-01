from django.db import models

# Create your models here.
class Employee(models.Model):
    """Represents an employee who can work in multiple teams."""
    id = models.AutoField(
            primary_key=True
        )
    # Fields
    Name = models.CharField(max_length=255, null=False)
    Team_Affiliation = models.CharField(max_length=255, null=True)
    Hourly_Rate = models.FloatField(null=False)
    
    def __str__(self) -> str:
        return self.Name

    class Meta:
        db_table = "employee"

class Team(models.Model):
    """Represents a Team."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    teamTitle = models.CharField(max_length=255, null=False)

    
class TeamLeader(models.Model):
    """Represents a TeamLeader."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leader')
    #A Team can only have one Leader
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class TeamEmployee(models.Model):
    """Represents a TeamEmployee."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    # 1:1 relation: one employee can be part of many teams
    member = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='member')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class WorkArrangement(models.Model):
    """Represents a Work Assignment which then worked by 1 team."""
    # Fields
    id = models.AutoField(
            primary_key=True
        )
    class Time(models.TextChoices):
        FT = 'Full Time'
        PT = 'Part Time'
        PT75 = 'Part Time 75%'
        PT50 = 'Part Time 50%'
        PT25 = 'Part Time 25%'

    employee = models.ForeignKey(TeamEmployee, on_delete=models.CASCADE, related_name='processed_by_employee')
    # work title

    # work title
    workTitle = models.CharField(max_length=255, null=False)
    # is employee works full time on this work assignment? 
    workedTime = models.CharField(max_length=255, choices=Time.choices)
