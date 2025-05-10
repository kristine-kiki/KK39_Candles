from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=300)
    friendly_name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ManyToManyField('Category')
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_bestseller = models.BooleanField(default=False, help_text="Display this on the homepage bestseller section?")

    def __str__(self):
        return self.name
    
    def update_average_rating(self):
        """
        Calculates the average rating from all Rating instances
        and updates the product's rating field.
        """
        average = self.ratings.all().aggregate(Avg('score'))['score__avg']
        if average is not None:
            self.rating = round(average, 2) 
        else:
            self.rating = None 
        self.save(update_fields=['rating']) # Efficiently save only the rating field
    
class Rating(models.Model):
    """
    Model to store individual user ratings for products.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_ratings")
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5), # Max rating of 5
            MinValueValidator(1)  # Min rating of 1
        ]
    )
    comment = models.TextField(max_length=500, null=True, blank=True) # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user') # User can only rate a product once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s rating for {self.product.name}: {self.score}/5"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving a rating, update the product's average rating
        self.product.update_average_rating()

    def delete(self, *args, **kwargs):
        product_to_update = self.product
        super().delete(*args, **kwargs)
        # After deleting a rating, update the product's average rating
        product_to_update.update_average_rating()
