from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'default_phone_number', 'default_street_address1',
            'default_street_address2', 'default_town_or_city',
            'default_county', 'default_postcode',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, classes, autofocus, remove labels,
        AND convert country choices to a list.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2 (Optional)',
            'default_county': 'County, State or Locality (Optional)',
        }

        first_field_name = next(iter(self.fields), None)
        if first_field_name and first_field_name in self.fields:
             self.fields[first_field_name].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            if field_name in placeholders:
                if field.required:
                    placeholder = f'{placeholders[field_name]} *'
                else:
                    placeholder = placeholders[field_name]
                field.widget.attrs['placeholder'] = placeholder

            css_classes = 'profile-input form-control'
            # No need for form-select logic here anymore
            field.widget.attrs['class'] = css_classes

            # Remove labels
            field.label = False