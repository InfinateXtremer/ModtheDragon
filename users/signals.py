from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import *

@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
