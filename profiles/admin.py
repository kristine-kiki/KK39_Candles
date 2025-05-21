from django.contrib import admin
from django.forms import Select                                      
from profiles.models import UserProfile
from django_countries.fields import CountryField                     

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

admin.site.register(UserProfile, UserProfileAdmin)