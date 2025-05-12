from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact/', views.contact, name='contact_us'),
    path('faq/', views.faq, name='faq'),
    path('shipping/', views.shipping, name='shipping_returns'),
    path('terms-service/', views.terms_service, name='terms_service'),
]
