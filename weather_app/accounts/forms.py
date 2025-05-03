from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator

class UserCreateForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Fields:", self.fields.keys())

        self.fields["username"].label = "Username"
        self.fields["username"].help_text = "150 characters or fewer"
        self.fields["email"].label = "Email Address"
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = "At least 8 characters"
        self.fields["password2"].label = "Confirm Password"

        # Add placeholder attributes for better UI
        for field in self.fields:
            self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})

    # Custom Email Validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    # Add Validators for Fields
    username = forms.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(3, message="Username must be at least 3 characters long."),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores.",
                code="invalid_username"
            )
        ]
    )

    email = forms.EmailField(
        validators=[
            EmailValidator(message="Enter a valid email address.")
        ]
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            MinLengthValidator(8, message="Password must be at least 8 characters long."),
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
                message="Password must contain a lower case letter, at least one uppercase letter, one number, and one special character.",
                code="invalid_password"
            )
        ]
    )
