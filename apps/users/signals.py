# organization/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def organization_created_handler(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] User created: {instance.username}")
    else:
        print(f"[Signal] User updated: {instance.username}")
