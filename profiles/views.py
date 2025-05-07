from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from checkout.models import Order

# Import the form from the same directory
#from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        #form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please check the form.')
    #else:
        #form = UserProfileForm(instance=profile)

    orders = Order.objects.filter(user_profile=profile).order_by('-date')

    template = 'profiles/profile.html'
    context = {
        #'form': form,
        'orders': orders,
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