from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import ContactForm

# Create your views here.

def contact(request):
    """
    Renders the 'Contact Us' page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form is valid, process the data
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email'] # User's email
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message']

            # Prepare email content
            email_subject = f'New Contact Form Message: {subject if subject else "Enquiry"}'
            email = render_to_string('contact/emails/email.html', {
                'name': name,
                'from_email': from_email,
                'subject': subject,
                'message_body': message_body,
            })
            email = f"Message from: {name} <{from_email}>\n\nSubject: {subject}\n\nMessage:\n{message_body}"

            try:
                send_mail(
                    subject=email_subject,
                    message=email, # Plain text version
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL], 
                    html_message=email, # HTML version (optional but nice)
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('contact:contact_us') 
            except Exception as e:
                messages.error(request, f'Sorry, there was an error sending your message: {e}. Please try again later or contact us directly via email.')

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact/contact_us.html', context)

def faq(request):
    """
    Renders the 'FAQ' page.
    """
    context = {}
    return render(request, 'contact/faq.html', context)

def shipping(request):
    """
    Renders the 'Shipping & Returns' page.
    """
    context = {}
    return render(request, 'contact/shipping_returns.html', context)

def terms_service(request):
    """
    Renders the 'Terms of Service' page.
    """
    context = {}
    return render(request, 'contact/terms_service.html', context)

def privacypolicy(request):
    """
    Renders the 'Terms of Service' page.
    """
    context = {}
    return render(request, 'contact/privacypolicy.html', context)