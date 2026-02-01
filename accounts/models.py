from django.db import models

ROLE_CHOICES = (
    ('student', 'Student'),
    ('staff', 'Staff/Mentor'),
    ('admin', 'Admin/Librarian'),
)

class Student(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    password = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    is_approved = models.BooleanField(default=False)   # ⭐ Added field

    def __str__(self):
        return self.username


class Staff(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    password = models.CharField(max_length=255)
    department = models.CharField(max_length=100)

    is_approved = models.BooleanField(default=False)   # ⭐ Added field

    def __str__(self):
        return self.username


class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    password = models.CharField(max_length=255)

    # ❌ NO is_approved HERE

    def __str__(self):
        return self.username


class Approval(models.Model):
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username
