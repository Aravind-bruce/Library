from django.db import models

class LoginRecord(models.Model):
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True, blank=True) 
    login_date = models.CharField(max_length=20)      # dd/mm/yyyy format
    login_time = models.CharField(max_length=20)      # IST time HH:MM:SS
    
    def __str__(self):
        return f"{self.username} - {self.login_date} {self.login_time}"
