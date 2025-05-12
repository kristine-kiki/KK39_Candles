from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email Address'})
    )
    subject = forms.CharField(
        max_length=150, 
        required=False, # Make subject optional, or True if required
        widget=forms.TextInput(attrs={'placeholder': 'Subject (Optional)'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5})
    )