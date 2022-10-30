from django.db import models

# Create your models here.
class Employee(models.Model):
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