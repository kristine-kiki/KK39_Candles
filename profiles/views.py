from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from checkout.models import Order
from django_countries.fields import CountryField
from .forms import UserProfileForm
from .models import WishlistItem
from products.models import Product


@login_required
def profile(request):
    """ Display the user's profile """

    profile_instance = get_object_or_404(UserProfile, user=request.user)
    country_choices_list = None # Initialize

    # --- Get choices directly from the Model Field ---
    try:
        country_field = UserProfile._meta.get_field('default_country')
        # Attempt to get choices from the field definition
        country_choices_list = list(country_field.choices)
        if country_field.blank:
             blank_label = getattr(country_field, 'blank_label', None) or ('', '---------') # Default blank tuple
             # Ensure blank label is a tuple
             if not isinstance(blank_label, (list, tuple)): blank_label = ('', blank_label)
             if not any(c[0] == blank_label[0] for c in country_choices_list):
                  country_choices_list.insert(0, blank_label)
                  print(f"DEBUG VIEW: Manually added blank choice: {blank_label}")

    except Exception as e:
        print(f"ERROR VIEW: Failed to get/process country choices from model field: {e}")
        country_choices_list = [('', 'Error loading countries')] # Provide fallback

    if request.method == 'POST':
        # Pass instance for update
        profile_form = UserProfileForm(request.POST, instance=profile_instance)
        if profile_form.is_valid():
            profile_form.save()

            country_code = request.POST.get('default_country')
            if country_code: # Check if a country was actually submitted
                 # Assign the submitted code directly to the instance field
                 profile_instance.default_country = country_code
                 # Save the instance again to persist the country change
                 profile_instance.save(update_fields=['default_country'])
                 print(f"DEBUG VIEW: Manually saved country code: {country_code}")

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile') 
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else: # GET request
        # Pass instance for initial display
        profile_form = UserProfileForm(instance=profile_instance)
        # country_choices_list was prepared above

    orders = profile_instance.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'form': profile_form, 
        'current_country': profile_instance.default_country,
        'orders': orders,
        'profile': profile_instance,
        'country_choices': country_choices_list, # Pass the prepared list
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """ Display a user's past order confirmation """
    order = get_object_or_404(Order, order_number=order_number)

    # Verify the order belongs to the requesting user
    if order.user_profile.user != request.user:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('profile')

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

@login_required
def view_wishlist(request):
    """ A view to display the user's wishlist """
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'profiles/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    """ Add a product to the user's wishlist """
    product = get_object_or_404(Product, id=product_id)
    # Check if item already in wishlist
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        messages.info(request, f"{product.name} is already in your wishlist!")
    else:
        WishlistItem.objects.create(user=request.user, product=product)
        messages.success(request, f"Added {product.name} to your wishlist.")
    
    # Redirect back to the previous page or product detail page
    return redirect(request.META.get('HTTP_REFERER', reverse('product_detail', args=[product.id])))

@login_required
def remove_from_wishlist(request, product_id):
    """ Remove a product from the user's wishlist """
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.filter(user=request.user, product=product)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f"Removed {product.name} from your wishlist.")
    else:
        messages.info(request, f"{product.name} was not in your wishlist.")
        
    # Redirect back to the wishlist page or previous page
    return redirect(request.META.get('HTTP_REFERER', reverse('view_wishlist')))
