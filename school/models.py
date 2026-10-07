from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)