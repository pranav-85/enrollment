from django.db import models

# Create your models here.

class Student():
    RollNumber : str
    Name : str
    CurrentSemester : int
    RegStatus : str

class Advisor():
    Advisor_ID : str
    Name : str

class Admin():
    Admin_ID : str
    Name : str

class StudentDoc():
    Name : str
    ID : str
    Document : str