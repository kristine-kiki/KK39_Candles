from django.urls import path
from . import views

urlpatterns = [
    path('our_story/', views.our_story_view, name='our_story'),
    path('ingredients/', views.ingredients_view, name='ingredients'),
]