from django.shortcuts import render

# Create your views here.

def contact(request):
    """
    Renders the 'Contact Us' page.
    """
    context = {}
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