from django.db import models
from django.contrib.auth.models import User # To link posts to an author
from django.urls import reverse
from django.utils.text import slugify # To generate URL-friendly slugs
from django.utils import timezone 
from django_summernote.fields import SummernoteTextField

class Post(models.Model):
    """
    Model for blog posts.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date', blank=True) # unique_for_date helps ensure unique URLs if titles are similar on different dates
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='about_blog_posts')
    content = SummernoteTextField()
    publish_date = models.DateTimeField(default=timezone.now) # When the post should be considered published
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='about_blog_images/', null=True, blank=True)

    class Meta:
        ordering = ('-publish_date',) # Order posts by publish date, newest first

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique for the publish date
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self): # Important for linking to individual posts
        return reverse('about:blog_post_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })