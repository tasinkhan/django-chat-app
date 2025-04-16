# organization/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Organization)
def organization_created_handler(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] Organization created: {instance.name}")
    # Log the organization creation
        logger.info(f"[Signal] Organization created: {instance.name}")
    else:
        print(f"[Signal] Organization updated: {instance.name}")
        # Log the organization update
        logger.info(f"[Signal] Organization updated: {instance.name}")
