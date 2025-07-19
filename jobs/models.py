from django.db import models
from profiles.models import User, Company

# Create your models here.


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applications')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class SavedJob(models.Model):
    saved_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class LikedJob(models.Model):
    liked_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_jobs')
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='liked_by')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} liked {self.job.title}"


class DislikedJob(models.Model):
    disliked_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='disliked_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='disliked_by')
    disliked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} disliked {self.job.title}"
