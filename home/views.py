from django.shortcuts import render
from products.models import Product

# Create your views here.

def home_view(request):
    bestseller_products = None
    try:
        # Limit to 4 bestsellers for the grid
        bestseller_products = Product.objects.filter(is_bestseller=True)[:4]
    except Product.DoesNotExist:
        bestseller_products = None
    except FieldError:
        print:("Error: 'is_bestseller' field not found on Product model.")
        bestseller_products = Product.objects.all().order_by('-id')[:4] 
    except Exception as e: # Catch potential field errors if is_bestseller isn't added yet
        print(f"Error fetching bestsellers (check Product model/query): {e}")
        bestseller_products = None # Fallback: random products


    context = {
        'bestseller_products': bestseller_products,
        # ... other context variables for your page ...
    }
    return render(request, 'home/index.html', context)

