from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.
class User(AbstractUser):
    Usertype = models.CharField(max_length=50)
    
    
    
class Department(models.Model):
    Dep_Name = models.CharField(max_length=100)
    
    
    
class Teacher(models.Model):
   dep_id = models.ForeignKey(Department,on_delete=models.CASCADE)
   teach_id = models.ForeignKey('User',on_delete=models.CASCADE)
   phone = models.BigIntegerField()
   Qualification = models.CharField(max_length=100, null=True, blank=True)
#    def __str__(self):
#         return f"{self.teacher_user.first_name} {self.teacher_user.last_name} - {self.department.Dep_Name}"   
   
class Student(models.Model):
    dep_id = models.ForeignKey(Department,on_delete=models.CASCADE)
    stud_id = models.ForeignKey('User',on_delete=models.CASCADE)
    Phone = models.BigIntegerField()
    place = models.CharField(max_length=100)
    
    
    
    
    
    
    
# # collegeapp/models.py
# class Teacher(models.Model):
#     phone = models.BigIntegerField()  # With parentheses
    # Other fields...
    
    
    
   

class Staff(models.Model):
    name=models.CharField(max_length=100)
    photo=models.ImageField(upload_to='staff_photo')
    

    
