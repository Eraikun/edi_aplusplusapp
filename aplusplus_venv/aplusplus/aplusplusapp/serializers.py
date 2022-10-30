from rest_framework import serializers
from django.db.models import fields
from .models import Employee


class AplusplusSerializer(serializers.ModelSerializer):
  # id = serializers.AutoField(primary_key=True)
  Name = serializers.CharField(max_length=255)
  Hourly_Rate = serializers.DecimalField(max_digits=6, decimal_places=2)
  def create(self, validated_data):
    # Once the request data has been validated, we can create a todo item instance in the database
    return Employee.objects.create(
      text=validated_data.get('text')
    )
  class Meta:
    model = Employee
    fields = (
      'id',
      'Name',
      'Hourly_Rate'
    )