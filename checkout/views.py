from decimal import Decimal
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.urls import NoReverseMatch # For safe redirects

from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents 

import stripe
import json
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY # Set Stripe API key globally for this module

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
        return handle_checkout_post(request)
    else:
        return handle_checkout_get(request, stripe_public_key)


def handle_checkout_post(request):
    """Handle POST requests to the checkout view for final order creation."""
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty. Payment was not processed.")
        return redirect(reverse('products'))

    form_data = extract_form_data(request.POST)
    order_form = OrderForm(form_data)

    if order_form.is_valid():
        try:
            pid = request.POST.get('client_secret', '').split('_secret')[0]
            if not pid:
                # This should ideally not happen if JS is working and client_secret is submitted
                messages.error(request, "Payment information was missing. Please try checking out again.")
                return redirect(reverse('checkout'))

            # Idempotency check: See if order already exists (e.g., created by webhook)
            order = Order.objects.filter(stripe_pid=pid).first()
            if order:
                messages.info(request, "Your order has already been processed.")
                cleanup_session(request) # Clear bag and save_info
                return redirect(reverse('checkout_success', args=[order.order_number]))

            # If order does not exist, create it
            order = create_order_from_form(order_form, request, bag, pid)
            create_order_line_items(order, bag)
            
            request.session['save_info'] = 'save-info' in request.POST
            # Success message is now in checkout_success to avoid duplication if order already existed
            
            return redirect(reverse('checkout_success', args=[order.order_number]))

        except Product.DoesNotExist:
            messages.error(request, "One of the products in your bag wasn't found. Payment may have been taken. Please contact support.")
            # Do not delete order if payment might have occurred
            return redirect(reverse('bag_view')) # Or a specific contact support page
        except ValueError as e: # From custom ValueErrors or issues like missing pid
            messages.error(request, str(e) or 'There was an error with your payment information. Please try again.')
            return redirect(reverse('checkout')) # Allow user to retry checkout
        except Exception as e:
            logger.error(f"Unexpected error in handle_checkout_post: {str(e)}", exc_info=True)
            messages.error(request, "An unexpected error occurred while placing your order. Payment may have been taken. Please contact support.")
            return redirect(reverse('bag_view')) # Or a specific contact support page
    else:
        # Form is invalid, re-render checkout page with form errors and a NEW PaymentIntent
        messages.error(request, 'There was an error with your form. Please double check your information.')
        
        current_bag_context = bag_contents(request)
        total = current_bag_context['grand_total']
        stripe_total = round(total * 100)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                payment_method_types=['card', 'paypal'],
            )
            client_secret_val = intent.client_secret
        except Exception as e:
            logger.error(f"Error re-creating PaymentIntent on POST form error: {str(e)}", exc_info=True)
            messages.error(request, "There was an issue re-initializing the payment form. Please try again.")
            return redirect(reverse('bag_view'))

        context = {
            'order_form': order_form, # The invalid form with errors
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': client_secret_val, # New client secret
            'grand_total': total,
        }
        return render(request, 'checkout/checkout.html', context)


def extract_form_data(post_data):
    """Extract form data from POST request."""
    return {
        'full_name': post_data.get('full_name', '').strip(),
        'email': post_data.get('email', '').strip(),
        'phone_number': post_data.get('phone_number', '').strip(),
        'country': post_data.get('country', '').strip(),
        'postcode': post_data.get('postcode', '').strip(),
        'town_or_city': post_data.get('town_or_city', '').strip(),
        'street_address1': post_data.get('street_address1', '').strip(),
        'street_address2': post_data.get('street_address2', '').strip(), # Use .get for optional
        'county': post_data.get('county', '').strip(), # Use .get for optional
    }


def create_order_from_form(order_form, request, bag, pid):
    """Create and save an Order instance from form data and payment ID."""
    order = order_form.save(commit=False)
    order.stripe_pid = pid # Set the Stripe PaymentIntent ID
    order.original_bag = json.dumps(bag)
    
    current_bag_context = bag_contents(request)
    order.order_total = current_bag_context['total']
    order.delivery_cost = current_bag_context['delivery']
    order.grand_total = current_bag_context['grand_total']

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order.user_profile = profile
        except UserProfile.DoesNotExist:
            # Handle case where profile might not exist even if user is auth (should not happen with signals)
            pass 
    order.save()
    return order


def create_order_line_items(order, bag):
    """Create OrderLineItem instances for each product in the bag."""
    for item_id, item_data_or_qty in bag.items():
        try:
            product = Product.objects.get(id=item_id) # Use id, not pk for consistency if item_id is str
            # Handle simple bag (item_id: quantity) vs complex bag (item_id: {'quantity': X, 'size': Y})
            # This logic depends heavily on your bag structure.
            # Assuming for now a simple structure or that bag_contents handles variants correctly
            # and the 'bag' in session for order creation might be simpler.
            # The original code implies item_data can be an int.
            if isinstance(item_data_or_qty, int):
                quantity = item_data_or_qty
                OrderLineItem.objects.create(order=order, product=product, quantity=quantity)
            elif isinstance(item_data_or_qty, dict) and 'quantity' in item_data_or_qty: # Example for a more complex bag
                quantity = item_data_or_qty['quantity']
                # order_line_item = OrderLineItem(order=order, product=product, quantity=quantity, product_size=item_data_or_qty.get('size'))
                OrderLineItem.objects.create(order=order, product=product, quantity=quantity)
            # Add more conditions if your bag stores items with variants differently
        except Product.DoesNotExist:
            logger.error(f"Product with id {item_id} not found during order line item creation for order {order.order_number}.")
            # This error will be caught by the caller (handle_checkout_post)
            raise Product.DoesNotExist 
            

def handle_checkout_get(request, stripe_public_key):
    """Handle GET requests to the checkout view, prepares the payment intent."""
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty")
        return redirect(reverse('products'))

    try:
        current_bag_context = bag_contents(request)
        total = current_bag_context['grand_total']
        stripe_total = round(total * 100)
        
        # Check for minimum amount
        # Ensure STRIPE_MINIMUM_AMOUNT_CENTS is in settings.py (e.g., 30 for £0.30)
        minimum_amount = getattr(settings, 'STRIPE_MINIMUM_AMOUNT_CENTS', 30) 
        if stripe_total < minimum_amount:
            error_msg = (f"The order total of £{total:.2f} is below the minimum "
                         f"amount of £{minimum_amount/100:.2f} required for payment processing. "
                         f"Please add more items to your bag.")
            logger.warning(f"Checkout attempt below minimum: Total {stripe_total} cents/pence. Minimum: {minimum_amount}")
            messages.error(request, error_msg)
            return redirect(reverse('bag_view'))
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        logger.info(f"Attempting to create PaymentIntent. Amount: {stripe_total}, Currency: {settings.STRIPE_CURRENCY}")
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            payment_method_types=['card', 'paypal'], # Enable PayPal
            metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
                'user_id': str(request.user.id) if request.user.is_authenticated else 'None',
                'integration_check': 'accept_a_payment'
            }
        )
        logger.info(f"PaymentIntent created successfully: {intent.id}")
        
        order_form = get_prefilled_order_form(request)
        
        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing from configuration. Payment will not work.')

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'grand_total': total, # For JS if needed (e.g. Apple Pay display)
        }
        return render(request, 'checkout/checkout.html', context)
    
    except stripe.error.StripeError as e:
        user_facing_error = "An issue occurred with our payment provider. Please try again or contact support."
        logger.error(f"StripeError in handle_checkout_get: {str(e)} (Code: {e.code if hasattr(e, 'code') else 'N/A'})", exc_info=True)
        if hasattr(e, 'user_message') and e.user_message:
            user_facing_error = e.user_message
        elif e.http_status == 402: 
            user_facing_error = "There was an issue with the payment details provided. Please check and try again."
        messages.error(request, user_facing_error)
        return redirect(reverse('bag_view'))
    except Exception as e:
        logger.error(f"Generic Exception in handle_checkout_get: {str(e)}", exc_info=True)
        messages.error(request, "Sorry, an unexpected error occurred while preparing your checkout. Please try again or contact support.")
        return redirect(reverse('bag_view'))

def get_prefilled_order_form(request):
    """Return an OrderForm prefilled with user profile data if available."""
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return OrderForm(initial={
                'full_name': profile.user.get_full_name() or '',
                'email': profile.user.email or '',
                'phone_number': profile.default_phone_number or '',
                'country': profile.default_country or '',
                'postcode': profile.default_postcode or '',
                'town_or_city': profile.default_town_or_city or '',
                'street_address1': profile.default_street_address1 or '',
                'street_address2': profile.default_street_address2 or '',
                'county': profile.default_county or '',
            })
        except UserProfile.DoesNotExist:
            logger.warning(f"UserProfile not found for authenticated user: {request.user.username}")
            return OrderForm(initial={'email': request.user.email or ''}) # At least prefill email
    return OrderForm()

# --- PayPal Return View ---
def stripe_paypal_return_view(request):
    """
    Landing page after user returns from PayPal.
    Client-side Stripe.js (on original checkout page) should handle PI confirmation.
    This view primarily checks status and redirects.
    """
    payment_intent_id = request.GET.get('payment_intent')
    pi_client_secret = request.GET.get('payment_intent_client_secret') # Stripe adds this

    if not payment_intent_id or not pi_client_secret:
        messages.error(request, "Invalid return from PayPal. Payment details incomplete.")
        return redirect(reverse('bag_view'))

    try:
        logger.info(f"PayPal return for PaymentIntent ID: {payment_intent_id}")
        # It's often better to let client-side JS (that initiated PayPal) handle confirmation using the client_secret.
        # This view can be a fallback or show a processing message.
        # For now, let's just try to retrieve and check status.
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == 'succeeded':
            if 'bag' in request.session:
                del request.session['bag']
                logger.info(f"PayPal Return: Bag cleared for user session after PI {payment_intent_id} success.")
            order = Order.objects.filter(stripe_pid=payment_intent_id).first()
            if order:
                if 'save_info' in request.session:
                    del request.session['save_info']
                return redirect(reverse('checkout_success', args=[order.order_number]))
            
            else:
                logger.warning(f"PayPal PI {payment_intent_id} succeeded but no order found. Waiting for webhook or user to complete checkout details if needed.")
                messages.info(request, "Your PayPal payment was successful! Your order is being processed and you will receive a confirmation email shortly. You can check your order history later.")
            try:
                return redirect(reverse('profiles:profile'))
            except NoReverseMatch:
                    logger.warning("NoReverseMatch for 'profiles:profile', falling back to 'home' for PayPal return.")
                    return redirect(reverse('home'))

        elif payment_intent.status == 'processing':
            messages.info(request, "Your PayPal payment is processing. You will receive a confirmation shortly.")
            # Redirect to a generic "order pending" or user's order history page
            try:
                return redirect(reverse, ('profiles:profile'))
            except NoReverseMatch:
                return redirect(reverse('home'))
        
    except stripe.error.StripeError as e:
        logger.error(f"StripeError in stripe_paypal_return_view for PI {payment_intent_id}: {str(e)}", exc_info=True)
        messages.error(request, f"Could not verify PayPal payment status: An error occurred with our payment provider.")
        return redirect(reverse('bag_view'))
    except Exception as e:
        logger.error(f"Generic Exception in stripe_paypal_return_view for PI {payment_intent_id}: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred while processing your PayPal return.")
        return redirect(reverse('bag_view'))

def safe_redirect_target(request, primary_target_name, fallback_target_name):
    """Helper to attempt redirect to primary target, fallback if NoReverseMatch."""
    try:
        return reverse(primary_target_name)
    except NoReverseMatch:
        logger.warning(f"NoReverseMatch for '{primary_target_name}', falling back to '{fallback_target_name}'.")
        return reverse(fallback_target_name)

# --- Success and Session Cleanup ---
def checkout_success(request, order_number):
    """Handle successful checkouts: save info, send messages, clean session."""
    try:
        order = get_object_or_404(Order, order_number=order_number)
        
        if request.user.is_authenticated:
            # Ensure profile exists before trying to attach
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if not order.user_profile: # Attach only if not already set (e.g., by webhook)
                order.user_profile = profile
                order.save()
            
            if request.session.get('save_info'): # Check before using
                save_user_info_to_profile(order, profile) # Use a helper
        
        send_success_message(request, order.order_number, order.email)
        cleanup_session(request)
        
        return render(request, 'checkout/checkout_success.html', {'order': order})
        
    except Exception as e:
        logger.error(f"Error in checkout_success for order {order_number}: {str(e)}", exc_info=True)
        messages.error(request, "There was an error displaying your order confirmation. Please check your profile for order details or contact support.")
        return redirect(reverse('home')) # Safe fallback

def save_user_info_to_profile(order, profile):
    """Helper to save order's shipping info to user's profile."""
    profile_data = {
        'default_phone_number': order.phone_number,
        'default_country': order.country,
        'default_postcode': order.postcode,
        'default_town_or_city': order.town_or_city,
        'default_street_address1': order.street_address1,
        'default_street_address2': order.street_address2,
        'default_county': order.county,
    }
    user_profile_form = UserProfileForm(profile_data, instance=profile)
    if user_profile_form.is_valid():
        user_profile_form.save()
    else:
        logger.error(f"Failed to save profile info for user {profile.user.username}: {user_profile_form.errors.as_json()}")


def send_success_message(request, order_number, email):
    """Send success message to user via Django messages."""
    messages.success(request, (
        f'Order successfully processed! Your order number is {order_number}. '
        f'A confirmation email will be sent to {email}.'
    ))

def cleanup_session(request):
    """Clean up session data after successful checkout."""
    if 'bag' in request.session:
        del request.session['bag']
    if 'save_info' in request.session: # Check before deleting
        del request.session['save_info']

# --- Stripe Webhook Data Caching ---
@require_POST
def cache_checkout_data(request):
    """
    Update PaymentIntent metadata. Called by JS before payment confirmation.
    """
    try:
        pid = request.POST.get('client_secret', '').split('_secret')[0]
        shipping_details_form_data = {
                    'full_name': request.POST.get('full_name', '').strip(),
                    'email': request.POST.get('email', '').strip(),
                    'phone_number': request.POST.get('phone_number', '').strip(),
                    'street_address1': request.POST.get('street_address1', '').strip(),
                    # ... other address fields
                    'country': request.POST.get('country', '').strip(),
                }
        print(f"--- Caching checkout data. Email from form: {shipping_details_form_data['email']} ---")
        if not pid:
            logger.error("cache_checkout_data: Missing client_secret in POST data.")
            return HttpResponse("Error: Missing client_secret.", status=400)
        
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info', 'false'), # String 'false' or 'true'
            'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
            'user_id': str(request.user.id) if request.user.is_authenticated else 'None',
            'customer_email': request.POST.get('email'),
        })
        return HttpResponse(status=200)
    except ValueError as e: # e.g. if client_secret format is wrong
        logger.error(f"ValueError in cache_checkout_data: {str(e)}", exc_info=True)
        return HttpResponse(content=str(e), status=400)
    except stripe.error.StripeError as e:
        logger.error(f"StripeError in cache_checkout_data for pid {pid if 'pid' in locals() else 'unknown'}: {str(e)}", exc_info=True)
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)
    except Exception as e:
        logger.error(f"Generic Exception in cache_checkout_data: {str(e)}", exc_info=True)
        messages.error(request, 'Sorry, there was an unexpected error. Please try again later.')
        return HttpResponse(content=str(e), status=400)