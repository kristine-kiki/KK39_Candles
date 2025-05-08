import json
import time
import logging
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError # Ensure BadHeaderError is imported
from django.template.loader import render_to_string
from django.conf import settings
from products.models import Product # Ensure your app name is correct
from profiles.models import UserProfile # Ensure your app name is correct
from .models import Order, OrderLineItem # Assuming this is from the 'checkout' app or similar
import stripe

logger = logging.getLogger(__name__)
print("WEBHOOK_HANDLER.PY MODULE LOADED") # To see if the module itself is loaded

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        print(f"StripeWH_Handler __init__ CALLED for request: {request.path}")

    def _send_confirmation_email(self, order):
        """
        Send order confirmation email with comprehensive error handling.
        Returns True if successful, False otherwise.
        """
        print(f"--- _send_confirmation_email CALLED for order ID: {order.id if order else 'NO ORDER OBJECT'} ---")
        try:
            if not order or not hasattr(order, 'email') or not order.email:
                print("--- _send_confirmation_email: Invalid order object, or order has no email attribute, or order.email is empty. ---")
                logger.error("Invalid order object (or missing/empty email) for email confirmation. Order: %s, Order Email: %s",
                             order.id if order else 'N/A', order.email if hasattr(order, 'email') else 'N/A')
                return False

            cust_email = order.email
            print(f"--- _send_confirmation_email: Customer email from order object: '{cust_email}' ---")

            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'order': order}
            ).strip() # Remove leading/trailing whitespace
            print(f"--- _send_confirmation_email: Rendered subject: '{subject}' ---")

            # Safely get DEFAULT_SUPPORT_PHONE from settings, providing a default if not found
            support_phone = getattr(settings, 'DEFAULT_SUPPORT_PHONE', 'N/A')

            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {
                    'order': order,
                    'contact_email': settings.DEFAULT_FROM_EMAIL,
                    'support_phone': support_phone # Use the safely retrieved value
                }
            )
            print(f"--- _send_confirmation_email: Rendered body (first 100 chars): '{body[:100]}...' ---")

            if not subject or not body:
                print("--- _send_confirmation_email: Empty email subject or body after rendering. ---")
                logger.error("Empty email subject or body for order %s", order.order_number)
                return False

            print(f"--- _send_confirmation_email: Attempting send_mail to '{cust_email}' from '{settings.DEFAULT_FROM_EMAIL}' ---")
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email],
                fail_silently=False # This will raise an exception on failure
            )
            # If using console.EmailBackend, the email content should be printed to the console by Django just before this line.
            print(f"--- _send_confirmation_email: SUCCESS - send_mail CALLED for '{cust_email}' (check console for email output) ---")
            logger.info(f"Confirmation email (should be on console) sent to {cust_email} for order {order.order_number}")
            return True
        
        except BadHeaderError:
            print("--- _send_confirmation_email: BadHeaderError ---")
            logger.error("Invalid header found in email for order %s", order.order_number if order else 'N/A', exc_info=True)
            return False
        except ConnectionError as e: # More specific than built-in ConnectionError
            print(f"--- _send_confirmation_email: Email server ConnectionError: {str(e)} ---")
            logger.error(f"Email server connection error for order {order.order_number if order else 'N/A'}: {str(e)}", exc_info=True)
            return False
        except TimeoutError: # Python's built-in TimeoutError
            print("--- _send_confirmation_email: Email sending TimeoutError ---")
            logger.error(f"Email sending timed out for order {order.order_number if order else 'N/A'}", exc_info=True)
            return False
        except Exception as e:
            print(f"--- _send_confirmation_email: UNEXPECTED EXCEPTION: {type(e).__name__} - {str(e)} ---")
            logger.error(f"Unexpected error sending confirmation email for order {order.order_number if order else 'N/A'}: {str(e)}", exc_info=True)
            return False

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        event_type = event.get("type", "Unknown type")
        print(f"--- handle_event CALLED for event type: {event_type} ---")
        logger.info(f'Unhandled webhook received: {event_type}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event_type}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        print("--- handle_payment_intent_succeeded CALLED ---")
        intent = event.data.object
        pid = intent.id
        print(f"--- handle_payment_intent_succeeded: Processing Intent ID {pid} ---")

        metadata = intent.get('metadata', {}) # Safer access to metadata
        bag_json = metadata.get('bag', '[]') # Get bag as JSON string
        save_info = metadata.get('save_info', 'false').lower() == 'true'
        username = metadata.get('username', 'AnonymousUser')

        # Check if charges data exists and is not empty
        billing_details = {}
        if hasattr(intent, 'charges') and intent.charges.data:
            billing_details = intent.charges.data[0].get('billing_details', {})
        
        shipping_details = intent.get('shipping') # This can be None
        grand_total = round(intent.amount / 100, 2)

        print(f"--- handle_payment_intent_succeeded: Billing Details: {billing_details} ---")
        print(f"--- handle_payment_intent_succeeded: Shipping Details: {shipping_details} ---")
        retrieved_email_from_billing = billing_details.get('email')
        print(f"--- handle_payment_intent_succeeded: Email from billing_details: '{retrieved_email_from_billing}' ---")

        # Clean data in the shipping details (only if shipping_details and its address exist)
        if shipping_details and shipping_details.address:
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

        profile = None
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info and shipping_details and shipping_details.address: # Ensure address exists
                    profile.default_phone_number = shipping_details.phone
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_county = shipping_details.address.state
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_country = shipping_details.address.country
                    profile.save()
                    print(f"--- handle_payment_intent_succeeded: Profile updated for user {username} ---")
            except UserProfile.DoesNotExist:
                print(f"--- handle_payment_intent_succeeded: UserProfile for {username} not found. ---")
                profile = None # Explicitly set to None

        order_exists = False
        order = None # Initialize order to None
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
                order_exists = True
                print(f"--- handle_payment_intent_succeeded: Order {order.order_number} (PID: {pid}) found in database. ---")
                break
            except Order.DoesNotExist:
                print(f"--- handle_payment_intent_succeeded: Order (PID: {pid}) not found. Attempt {attempt}. Sleeping... ---")
                attempt += 1
                time.sleep(1)
        
        if order_exists:
            print(f"--- handle_payment_intent_succeeded: Verified order {order.order_number} already exists. Attempting to send confirmation email. ---")
            email_sent_status = self._send_confirmation_email(order)
            print(f"--- handle_payment_intent_succeeded: Email sent status for existing order {order.order_number}: {email_sent_status} ---")
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            print(f"--- handle_payment_intent_succeeded: Order (PID: {pid}) does not exist. Creating new order. ---")
            try:
                # Prepare order data safely
                order_data = {
                    'user_profile': profile,
                    'email': billing_details.get('email', ''), # Comes from billing details
                    'original_bag': bag_json,
                    'stripe_pid': pid,
                    'order_total': grand_total, # This might need adjustment based on bag items sum + delivery
                    'delivery_cost': 0,  # TODO: Adjust as needed or calculate
                    'grand_total': grand_total,
                }

                # Safely add shipping details if available
                if shipping_details:
                    order_data['full_name'] = shipping_details.get('name', billing_details.get('name', ''))
                    order_data['phone_number'] = shipping_details.get('phone', billing_details.get('phone', ''))
                    if shipping_details.address:
                        order_data.update({
                            'street_address1': shipping_details.address.get('line1', ''),
                            'street_address2': shipping_details.address.get('line2', ''),
                            'town_or_city': shipping_details.address.get('city', ''),
                            'county': shipping_details.address.get('state', ''),
                            'postcode': shipping_details.address.get('postal_code', ''),
                            'country': shipping_details.address.get('country', ''),
                        })
                else: # Fallback if no shipping details at all
                    order_data['full_name'] = billing_details.get('name', '')
                    order_data['phone_number'] = billing_details.get('phone', '')
                
                print(f"--- handle_payment_intent_succeeded: Order data for creation: {order_data} ---")
                order = Order.objects.create(**order_data)
                print(f"--- handle_payment_intent_succeeded: New order {order.order_number} (ID: {order.id}) CREATED. ---")

                # Process bag items
                try:
                    bag = json.loads(bag_json)
                    for item_id, item_data in bag.items():
                        product = Product.objects.get(id=item_id)
                        # Assuming item_data can be just quantity (int) or a dict with quantity
                        if isinstance(item_data, int):
                            quantity = item_data
                        elif isinstance(item_data, dict):
                            quantity = item_data.get('quantity', 0) # Or however quantity is stored
                        else:
                            logger.warning(f"Unknown item_data format in bag for item_id {item_id}: {item_data}")
                            continue # Skip this item or handle error

                        if quantity > 0:
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                            )
                            order_line_item.save()
                            print(f"--- handle_payment_intent_succeeded: Created OrderLineItem for product {product.id}, quantity {quantity} for order {order.id} ---")
                except json.JSONDecodeError:
                    logger.error(f"Error decoding bag JSON for order {order.id}: {bag_json}", exc_info=True)
                    # Decide if order should be deleted or marked as needing attention
                except Product.DoesNotExist:
                    logger.error(f"Product with id {item_id} not found while creating line items for order {order.id}", exc_info=True)
                    # Decide if order should be deleted or marked as needing attention
                except Exception as e_li: # More specific exception for line item creation
                    logger.error(f"Error creating line items for order {order.id}: {str(e_li)}", exc_info=True)
                    # Decide if order should be deleted or marked as needing attention

            except Exception as e_order: # General exception for order creation
                print(f"--- handle_payment_intent_succeeded: ERROR creating order: {type(e_order).__name__} - {str(e_order)} ---")
                logger.error(f'Webhook received: {event["type"]} | ERROR creating order: {e_order}', exc_info=True)
                if order and order.id: # If order object was partially created and has an ID
                    print(f"--- handle_payment_intent_succeeded: Deleting partially created order {order.id} due to error. ---")
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e_order}',
                    status=500)
        
        # This part is reached if order_exists was False and order creation succeeded (or was None and failed silently before)
        if order: # Ensure order object is valid before sending email
            print(f"--- handle_payment_intent_succeeded: Attempting to send confirmation for newly created order {order.order_number}. ---")
            email_sent_status = self._send_confirmation_email(order)
            print(f"--- handle_payment_intent_succeeded: Email sent status for new order {order.order_number}: {email_sent_status} ---")
        else:
            # This case should ideally be caught by the order creation try/except block
            print(f"--- handle_payment_intent_succeeded: Order object is None after creation logic. Cannot send email. PID: {pid} ---")
            logger.error(f"Order object is None after creation logic for PID {pid}. Email not sent.")
            # Return a 500 because an order should have been created but wasn't, indicating an issue.
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order creation failed silently.',
                status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook and attempted email.',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        event_type = event.get("type", "Unknown type")
        print(f"--- handle_payment_intent_payment_failed CALLED for event type: {event_type} ---")
        logger.info(f'Webhook received (payment failed): {event_type}')
        return HttpResponse(
            content=f'Webhook received: {event_type}',
            status=200)