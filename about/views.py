from django.shortcuts import render

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