from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from products.models import Product

# Create your models here.

class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        """Returns the user's full name"""
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def email(self):
        """Returns the user's email"""
        return self.user.email
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """
        Create or update the user profile
        """
        if created:
            UserProfile.objects.create(user=instance)
        else:
            try:
                instance.userprofile.save()
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=instance)
            except AttributeError:
                UserProfile.objects.create(user=instance)

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Ensures a user can only add a product once to their wishlist
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"        