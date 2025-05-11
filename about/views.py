from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.

def our_story_view(request):
    """
    Renders the 'Our Story' page.
    """
    context = {}
    return render(request, 'about/our_story.html', context)

def ingredients_view(request):
    """
    Renders the 'Ingredients' page.
    """
    context = {}
    return render(request, 'about/ingredients.html', context)

def blog_list_view(request):
    """
    Displays a list of published blog posts, with pagination.
    """
    object_list = Post.objects.filter(status='published').order_by('-publish_date')
    paginator = Paginator(object_list, 5) # Show 5 posts per page
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'page_title': 'Our Blog', # You can use this in the template <title>
        'posts': posts,
    }
    return render(request, 'about/blog_list.html', context)

def blog_post_detail_view(request, year, month, day, slug):
    """
    Displays a single blog post.
    """
    post = get_object_or_404(Post, 
                             slug=slug,
                             status='published',
                             publish_date__year=year,
                             publish_date__month=month,
                             publish_date__day=day)
    context = {
        'post': post,
    }
    return render(request, 'about/blog_post_detail.html', context)