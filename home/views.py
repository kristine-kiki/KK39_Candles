from django.shortcuts import render
from products.models import Product
from django.contrib import messages

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
        bestseller_products = None 

    context = {
        'bestseller_products': bestseller_products,
    }

    return render(request, 'home/index.html', context)

def newsletter_thanks(request):
    messages.success(request, 'Thank you for subscribing to our newsletter!')

    return render(request, 'home/newsletter_thanks.html')

