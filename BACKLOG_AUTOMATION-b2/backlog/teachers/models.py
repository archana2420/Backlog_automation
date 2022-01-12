from django.db import models

# Create your models here.
class staff_details(models.Model):
    email=models.EmailField(max_length=32)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.email