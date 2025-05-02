
# import stripe # Commented out Stripe import
import json
from decimal import Decimal

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
# from django.views.decorators.http import require_POST # Commented out - not needed without cache_checkout_data
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

# Create your views here.

# @require_POST # Commented out - this view is not needed without Stripe metadata
# def cache_checkout_data(request):
#     """
#     Placeholder for caching data - Stripe functionality removed for now.
#     """
#     try:
#         # pid = request.POST.get('client_secret').split('_secret')[0] # Stripe specific
#         # stripe.api_key = settings.STRIPE_SECRET_KEY # Stripe specific
#         # stripe.PaymentIntent.modify(pid, metadata={ ... }) # Stripe specific
#         print("DEBUG: cache_checkout_data called (Stripe functionality removed)")
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, ('Sorry, there was an issue preparing your '
#                                  'checkout. Please try again later.'))
#         print(f"Error in placeholder cache_checkout_data: {e}")
#         return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handle the main checkout process (display form, process order).
    Stripe functionality commented out for now.
    """
    # stripe_public_key = settings.STRIPE_PUBLIC_KEY # Stripe specific
    # stripe_secret_key = settings.STRIPE_SECRET_KEY # Stripe specific

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False) # Don't save yet

            # --- Stripe Payment ID handling removed ---
            # pid = request.POST.get('client_secret').split('_secret')[0]
            # order.stripe_pid = pid
            # ------------------------------------------

            order.original_bag = json.dumps(bag)

            # Calculate totals using bag_contents
            current_bag_context = bag_contents(request)
            order.order_total = current_bag_context['total']
            order.delivery_cost = current_bag_context['delivery']
            order.grand_total = current_bag_context['grand_total']

            # --- Assume order is valid without payment for now ---
            # In a real scenario, payment confirmation would happen before this point.
            order.save() # Save the order

            # --- Create OrderLineItem instances ---
            try:
                for item_id, item_data in bag.items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order, product=product, quantity=item_data)
                        order_line_item.save()

            except Product.DoesNotExist:
                 messages.error(request, ("One of the products in your bag wasn't found."))
                 order.delete()
                 return redirect(reverse('view_bag'))
            except Exception as e:
                 messages.error(request, "An error occurred creating your order items. Please try again.")
                 print(f"Error creating line items: {e}")
                 order.delete()
                 return redirect(reverse('view_bag'))

            # request.session['save_info'] = 'save-info' in request.POST # Optional save info logic

            messages.success(request, f'Order successfully placed! Your order number is {order.order_number}.')
            if 'bag' in request.session:
                del request.session['bag']

            return redirect(reverse('checkout_success', args=[order.order_number]))

        else: # Form invalid
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
            # No redirect, re-render page with errors

    # --- GET Request ---
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        # --- Stripe PaymentIntent creation removed ---
        # current_bag_context = bag_contents(request)
        # total = current_bag_context['grand_total']
        # stripe_total = round(total * 100)
        # stripe.api_key = stripe_secret_key
        # intent = stripe.PaymentIntent.create(...)
        # -------------------------------------------

        order_form = OrderForm()

    # --- Warning for Stripe key removed ---
    # if not stripe_public_key:
    #    messages.warning(request, ('Stripe public key is missing.'))
    # --------------------------------------

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        # --- Stripe keys removed from context ---
        # 'stripe_public_key': stripe_public_key,
        # 'client_secret': intent.client_secret, # Removed
        # --------------------------------------
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts (no payment confirmation needed here yet)
    """
    # save_info = request.session.get('save_info') # Optional save info
    order = get_object_or_404(Order, order_number=order_number)

    # Optional: Attach order to user's profile
    # ...

    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    # if 'save_info' in request.session: # Optional
    #     del request.session['save_info']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)



