from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,) # Display line items within the Order view

    # Fields that should not be editable after order creation
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total', 'grand_total',
                       'original_bag', 'stripe_pid')
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total',)

    list_filter = ('date',)

    search_fields = ('order_number', 'full_name', 'email',)

    ordering = ('-date',)

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'date', 'user_profile') # Add user_profile if using
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Shipping Address', {
            'fields': ('street_address1', 'street_address2', 'town_or_city',
                    'county', 'postcode', 'country')
        }),
        ('Financials', {
            'fields': ('order_total', 'delivery_cost', 'grand_total')
        }),
        ('Stripe Info', {
            'fields': ('original_bag', 'stripe_pid')
        }),
    )

admin.site.register(Order, OrderAdmin)