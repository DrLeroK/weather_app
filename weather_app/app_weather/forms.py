from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

class WeatherForm(forms.Form):
    city = forms.CharField(
        label='Enter City',
        max_length=100,
        validators=[
            MinLengthValidator(2, message="City name must be at least 2 characters long."),
            MaxLengthValidator(100, message="City name cannot exceed 100 characters."),
            RegexValidator(
                regex=r'^[A-Za-z\s-]+$',
                message="City name must contain only letters, spaces, or hyphens.",
                code='invalid_city'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter city name'})
    )
