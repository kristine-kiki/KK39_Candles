from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from products.models import Product

# Create your views here.

def bag_view(request):
    bag_items = []
    total = Decimal(0)
    for item_id, quantity in request.session.get('bag', {}).items():
        product = get_object_or_404(Product, pk=item_id)
        line_total = Decimal(quantity)*product.price
        total += line_total
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'line_total': quantity * product.price,
        })

    delivery_threshold = Decimal(75)
    delivery_percentage = Decimal(settings.STANDART_DELIVERY_PERCENTAGE) / Decimal(100)
    delivery = Decimal(0) if total >= delivery_threshold else total * delivery_percentage

    subtotal = sum(item['line_total'] for item in bag_items)

    context = {
        'bag_items': bag_items,
        'subtotal': total,
        'delivery': delivery,
        'free_delivery_delta': 75 - sum(item['line_total'] for item in bag_items),
        'grand_total': subtotal + delivery,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ add a quantity of the specified product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(request.META.get('HTTP_REFERER', reverse('products')))

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    # Ensure product exists (optional but good practice)
    product = get_object_or_404(Product, pk=item_id)
    try:
        quantity = int(request.POST.get('quantity'))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity specified.')
        return redirect(reverse('bag_view'))

    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        # Remove item if quantity is 0 or less
    
    else:
        if item_id in bag:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('bag_view')) # Redirect back to the bag page

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        # Ensure product exists (optional)
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        if item_id in bag:
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')
        else:
            messages.error(request, "Item is not found in your bag")

        request.session['bag'] = bag
        return redirect(reverse('bag_view')) # Redirect back to the bag page

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)