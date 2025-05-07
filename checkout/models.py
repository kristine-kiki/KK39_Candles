from django.db import models
import uuid # For generating unique order numbers
from decimal import Decimal # For financial calculations
from django.db import models
from django.db.models import Sum
from django.conf import settings # To access settings like delivery thresholds
from django_countries.fields import CountryField # For the country field
from products.models import Product # Import your Product model
from profiles.models import UserProfile


# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    # Shipping Address
    street_address1 = models.CharField(max_length=100, null=False, blank=False)
    street_address2 = models.CharField(max_length=100, null=True, blank=True)
    town_or_city = models.CharField(max_length=50, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True) # Optional
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False) # Use django-countries
    # Order Details
    date = models.DateTimeField(auto_now_add=True) # Automatically set when order is created
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0) # Subtotal of items
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0) # Final cost
    # Fields for auditing or payment integration
    original_bag = models.TextField(null=False, blank=False, default='') # Store bag content as JSON text
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='') # Stripe Payment Intent ID

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        Called from OrderLineItem's save method.
        """
        # Calculate order_total (subtotal) by summing lineitem totals
        # Uses the 'lineitems' related_name from OrderLineItem ForeignKey
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or Decimal('0.00')

        # Calculate delivery cost (example logic, adapt as needed)
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            delivery_percentage = Decimal(settings.STANDART_DELIVERY_PERCENTAGE) / 100
            self.delivery_cost = self.order_total * delivery_percentage
        else:
            self.delivery_cost = Decimal('0.00')

        # Calculate grand total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE) # Or models.PROTECT
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False) # Calculated: quantity * product.price

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        # Calculate the total for this line item (uses current product price)
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        # Update the Order's totals after saving the line item

    def __str__(self):
        return f'Product {self.product.name} (ID: {self.product.id}) on order {self.order.order_number}'