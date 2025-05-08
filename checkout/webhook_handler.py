import json
import time
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem
import stripe

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata if hasattr(intent, 'metadata') else {}
        bag = metadata.get('bag', '[]')
        save_info = metadata.get('save_info', 'false') == 'true'
        username = metadata.get('username', 'AnonymousUser')

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        ) if hasattr(intent, 'latest_charge') else None

        billing_details = intent.charges.data[0].billing_details if hasattr(intent, 'charges') else {}
        shipping_details = intent.shipping if hasattr(intent, 'shipping') else {}
        grand_total = round(intent.amount / 100, 2)

        # Clean data in the shipping details
        if shipping_details:
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info and shipping_details:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_county = shipping_details.address.state
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_country = shipping_details.address.country
                    profile.save()
            except UserProfile.DoesNotExist:
                profile = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.get('name', ''),
                    user_profile=profile,
                    email=billing_details.get('email', ''),
                    phone_number=shipping_details.get('phone', ''),
                    street_address1=shipping_details.address.get('line1', '') if shipping_details else '',
                    street_address2=shipping_details.address.get('line2', '') if shipping_details else '',
                    town_or_city=shipping_details.address.get('city', '') if shipping_details else '',
                    county=shipping_details.address.get('state', '') if shipping_details else '',
                    postcode=shipping_details.address.get('postal_code', '') if shipping_details else '',
                    country=shipping_details.address.get('country', '') if shipping_details else '',
                    original_bag=bag,
                    stripe_pid=pid,
                    order_total=grand_total,
                    delivery_cost=0,  # Adjust as needed
                    grand_total=grand_total,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)