from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total calculation when a line item is updated/created.
    """
    instance.order.update_total() # Call the update_total method on the related Order


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total calculation when a line item is deleted.
    """
    # Note: instance.order should still be accessible here as the instance
    # holds the data just before deletion.
    instance.order.update_total() # Call the update_total method on the related Order