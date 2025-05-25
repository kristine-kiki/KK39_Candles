from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models.functions import Lower
from django.db.models import Q
from .models import Product, Category, Rating
from .forms import ProductForm, RatingForm
from profiles.models import WishlistItem

# Create your views here.

def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            if 'for_home' in categories:
                products = products.filter(category__name='for_home').exclude(category__name='candles')
            elif 'candles' in categories:
                products = products.filter(category__name='candles').exclude(category__name='for_home')
            else:
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You need to enter search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'wishlist_product_ids': wishlist_product_ids,
    }

    return render(request, 'products/products.html', context)

def home_view(request):
    bestseller_products = Product.objects.filter(is_bestseller=True)[:4]
    context = {
        'bestseller_products': bestseller_products,
    }
    return render(request, 'home/index.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    ratings = Rating.objects.filter(product=product).order_by('-created_at') # Get existing ratings
    
    existing_rating_by_user = None
    is_in_wishlist = False # Default to False
    if request.user.is_authenticated:
        existing_rating_by_user = Rating.objects.filter(product=product, user=request.user).first()
        if WishlistItem.objects.filter(user=request.user, product=product).exists():
            is_in_wishlist = True

    if request.method == 'POST':
        # Ensure user is authenticated before processing the form
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to submit a rating.")
            # Redirect to login, then back to product? Or just show error.
            # For simplicity, let's redirect to the product page, the template will show login link.
            return redirect('product_detail', product_id=product.id)

        # If user has already rated, prevent new submission (unless you want to allow updates)
        if existing_rating_by_user:
            messages.info(request, "You have already rated this product.")
            return redirect('product_detail', product_id=product.id)

        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save() # This will trigger product.update_average_rating()
            messages.success(request, f"Thank you for rating {product.name}!")
            return redirect('product_detail', product_id=product.id) # Redirect to refresh and see new rating
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
            # We'll pass this invalid form to the template to show errors
    else:
        # For GET request, provide an empty form
        rating_form = RatingForm()

    context = {
        'product': product,
        'ratings': ratings, # All ratings for this product
        'rating_form': rating_form,
        'existing_rating_by_user': existing_rating_by_user,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'products/products_detail.html', context)


@login_required
def add_product(request):
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {'form': form}

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated product: {product.name}!')
            return redirect('product_detail', product_id=product.id) # Or redirect
        else:
            messages.error(request, f'Failed to update product. Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing "{product.name}"')

    template = 'products/add_product.html'
    context = {'form': form, 'product': product}

    return render(request, template, context)

def index(request):
    featured_products = Product.objects.filter(is_featured=True)
    for p in featured_products:
        print(f"Featured Product: {p.name}, ID: {p.id}") # Debug print
    context = {'featured_products': featured_products}
    return render(request, 'home/index.html', context)

@login_required 
def add_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the user has already rated this product
    existing_rating = Rating.objects.filter(product=product, user=request.user).first()

    if existing_rating:
        messages.info(request, "You have already rated this product.")
        
        form = RatingForm(instance=existing_rating)
        return redirect('product_detail', product_id=product.id) # Redirect to product detail page

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False) 
            rating.product = product
            rating.user = request.user
            rating.save() # This will now trigger the update_average_rating on Product
            messages.success(request, f"Thank you for rating {product.name}!")
            return redirect('product_detail', product_id=product.id) # Redirect to product detail page
        else:
            messages.error(request, "There was an error with your rating. Please check the form.")
    else:
        form = RatingForm()

    context = {
        'form': form,
        'product': product,
        'existing_rating': existing_rating # Pass this to template to conditionally show form or message
    }

    return render(request, 'products/add_rating.html', context)

def product_search(request):
    query_text = None
    results = []
    search_performed = False

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True))

    if 'q' in request.GET:
        search_performed = True
        query_text = request.GET.get('q').strip()
        
        if query_text: 
            vector = SearchVector('name', weight='A') + \
                     SearchVector('description', weight='B') + \
                     SearchVector('category__name', weight='C') + \
                     SearchVector('category__friendly_name', weight='C')
            
            search_query_obj = SearchQuery(query_text, search_type='websearch')
            
            results = Product.objects.annotate(
                search=vector,  # Annotate the queryset with the search vector, aliased as 'search'
                rank=SearchRank(vector, search_query_obj)
            ).filter(search=search_query_obj, rank__gte=0.01).order_by('id','-rank').distinct('id')

            if not results.exists():
                messages.info(request, f"No products found matching '{query_text}'.")
        
        else:
            messages.error(request, "Please enter a search term.")
            
    context = {
        'query': query_text,
        'results': results,
        'search_performed': search_performed,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'products/search_results.html', context)