from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(default='1900-01-01', blank=False, null=False)  # Set a default date
    email = models.EmailField(default='example@example.com', blank=False, null=False)  # Set a default email

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(Student, related_name='courses')
    course_id = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return self.name


