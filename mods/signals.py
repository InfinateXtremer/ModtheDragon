from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from .models import *

@receiver(pre_save, sender=Mod)
def build_profile(sender, instance, update_fields):
	print(update_fields)
	if instance.file and update_fields:
		pass
