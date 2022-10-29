from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.AutoField(
            primary_key=True
        )
    # Fields
    Name = models.CharField(max_length=255, null=False)
    Hourly_Rate = models.FloatField(null=False)

    class Meta:
        db_table = "Employee"