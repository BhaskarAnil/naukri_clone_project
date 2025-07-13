from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Company


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer:
            Company.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)
