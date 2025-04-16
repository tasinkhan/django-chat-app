# organization/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization

@receiver(post_save, sender=Organization)
def organization_created_handler(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] Organization created: {instance.name}")
    else:
        print(f"[Signal] Organization updated: {instance.name}")
