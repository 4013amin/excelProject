# models.py
from django.db import models

class Employee(models.Model):
    personal_code = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    insurance_date = models.DateField()
    address = models.TextField()
    contract_duration = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.personal_code}"
