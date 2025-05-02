from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products .models import Product

def bag_contents(request):

    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        
        try:
            product_count += item_data
            product = get_object_or_404(Product, pk=item_id)
            line_total = item_data * product.price
            total += line_total
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'line_total': line_total 
            })

        except Product.DoesNotExist:
            # Handle case where product might have been deleted but is still in session bag
            print(f"Warning: Product with id {item_id} not found, skipping.")

    delivery = Decimal('0.00')
    free_delivery_delta = Decimal('0.00')

    if total > 0: # Calculate delivery only if there's a subtotal
        # Use Decimal for settings values too if possible, otherwise cast
        free_delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
        standart_delivery_percentage = Decimal(settings.STANDART_DELIVERY_PERCENTAGE)

        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = total * Decimal(settings.STANDART_DELIVERY_PERCENTAGE / 100)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = Decimal('0.00')
            free_delivery_delta = Decimal('0.00')
    else:
         delivery = Decimal('0.00')
         free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD) # Show full threshold needed if bag is empty

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context