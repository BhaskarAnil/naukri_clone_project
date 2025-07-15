from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    is_employer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mobile = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, db_column='user_id', related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    resume_url = models.URLField(max_length=255, blank=True)

    def __str__(self):
         return self.user.username 


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, db_column='user_id')
    company_name = models.CharField(max_length=255, blank=True)
    company_logo_url = models.URLField(max_length=512, blank=True, null=True, help_text="Paste a public Google Drive image link.")
    description = models.TextField(blank=True)

    def __str__(self):
         return self.user.username 
