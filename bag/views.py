from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

# Create your views here.

def bag_view(request):
    
    return render(request,'bag/bag.html')

def add_to_bag(request, item_id):
    """ add a quantity of the specified product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')
    bag = request.session.get('bag', {})
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    # Ensure product exists (optional but good practice)
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    bag = request.session.get('bag', {})

    if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        # Remove item if quantity is 0 or less
    bag.pop(item_id)
    messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('bag_view')) # Redirect back to the bag page

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        # Ensure product exists (optional)
        product = get_object_or_404(Product, pk=item_id)
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('bag_view')) # Redirect back to the bag page

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)