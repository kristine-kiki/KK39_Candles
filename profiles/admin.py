from django.contrib import admin
from django.forms import Select                                      
from profiles.models import UserProfile
from django_countries.fields import CountryField
from .models import WishlistItem                     

# Create a custom ModelAdmin for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {
        CountryField: {'widget': Select}, 
    }

    list_display = ('user', 'default_country', 'default_phone_number')
    readonly_fields = ('user',) 

    try:
        admin.site.unregister(UserProfile)
    except admin.sites.NotRegistered:
        pass

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_on')
    list_filter = ('user', 'added_on')
    search_fields = ('user__username', 'product__name')

admin.site.register(UserProfile, UserProfileAdmin)