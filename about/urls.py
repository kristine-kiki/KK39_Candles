from django.urls import path
from . import views

app_name = 'about' 

urlpatterns = [
    path('our_story/', views.our_story_view, name='our_story'),
    path('ingredients/', views.ingredients_view, name='ingredients'),
    path('blog/', views.blog_list_view, name='blog_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.blog_post_detail_view, name='blog_post_detail'),
]