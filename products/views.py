from django.shortcuts import render
from .models import Product

# Create your views here.

def all_products(request):
    return render(request, 'products/products.html')

def product_detail(request, product_id):
    """ A view to show individual product details """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/product_detail.html', context)

"""
@login_required
def add_product(request):
     Add a product to the store
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
"""
