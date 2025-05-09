from django import forms
from .widgets import CustomClearableFileInput 
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances,
    styled for the KK39 Candles project.
    """

    class Meta:
        model = Product
        fields = '__all__' # Includes all fields from the Product model
        
        # define widgets 
        # or override them below for more complex logic or dynamic choices.
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Candle Name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the candle...'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'sku': forms.TextInput(attrs={'placeholder': 'SKU123'}),
            'stock_quantity': forms.NumberInput(attrs={'placeholder': '0'}),
        }

    # Override the image field to use your custom widget and set label
    # The 'required=False' is good as the image might already exist for an update.
    image = forms.ImageField(
        label='Product Image',
        required=False,
        widget=CustomClearableFileInput # Your custom widget for better image handling
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate category choices with friendly names
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        if self.fields.get('category'): # Check if 'category' field exists
            self.fields['category'].choices = friendly_names

        # Apply consistent styling and placeholders to all fields
        # Using styles similar to your login/auth forms
        default_input_class = 'form-control kk39-input' # Main class for most inputs
        default_select_class = 'form-control kk39-select' # Main class for select
        default_textarea_class = 'form-control kk39-textarea' # Main class for textarea
        default_checkbox_class = 'form-check-input kk39-checkbox' # For checkboxes
        default_file_class = 'form-control-file kk39-file-input' # For file inputs

        for field_name, field in self.fields.items():
            # Add a common class for global styling, if needed
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' kk39-form-field'

            if field_name == 'image':
                field.widget.attrs['class'] = default_file_class
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = default_checkbox_class
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = default_textarea_class
                field.widget.attrs['rows'] = 4 # Default rows for textareas
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = default_select_class
            else: # Default for TextInput, NumberInput, EmailInput, etc.
                field.widget.attrs['class'] = default_input_class

            # Add placeholders (customize these based on your Product model fields)
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'E.g., Lavender Dream Candle'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Enter a detailed description of the candle, its scent, materials, etc.'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
            elif field_name == 'sku':
                field.widget.attrs['placeholder'] = 'E.g., KK39-LAV-001'
            elif field_name == 'stock_quantity':
                field.widget.attrs['placeholder'] = 'Enter current stock level'
                # field.widget.attrs['min'] = '0'
            elif field_name == 'weight_grams': # Example field
                field.widget.attrs['placeholder'] = 'E.g., 250'
            
            if field.required:
                field.widget.attrs['class'] += ' is-required-field'


        # Specific styling for the category field if it's a Select widget
        if self.fields.get('category') and isinstance(self.fields['category'].widget, forms.Select):
            self.fields['category'].widget.attrs['class'] = default_select_class
        
        
        if 'rating' in self.fields:
            self.fields['rating'].widget = forms.NumberInput(attrs={
                'class': default_input_class,
                'min': '0',
                'max': '5',
                'step': '0.1',
                'placeholder': '0.0 - 5.0'
            })