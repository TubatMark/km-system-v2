from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with necessary fields."""

    # Add first_name and last_name as required fields
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter first name"}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter last name"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "middle_name",
            "institution",
            "position",
            "date_birth",
            "sex",
            "gender",
            "specialization",
            "highest_educ",
            "contact_num",
            "user_type",
            "note",
        )
        widgets = {
            "date_birth": forms.DateInput(attrs={"type": "date"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email address"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter middle name"}
            ),
            # Add more widgets as needed for consistent styling
        }

    def clean_email(self):
        """Ensure email is unique before saving."""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_first_name(self):
        """Clean and validate first name."""
        first_name = self.cleaned_data.get("first_name")
        if not first_name or not first_name.strip():
            raise forms.ValidationError("First name is required.")
        return first_name.strip()

    def clean_last_name(self):
        """Clean and validate last name."""
        last_name = self.cleaned_data.get("last_name")
        if not last_name or not last_name.strip():
            raise forms.ValidationError("Last name is required.")
        return last_name.strip()


class CustomUserUpdateForm(UserChangeForm):
    """Form for updating user information (excluding password)."""

    password = None  # Hides the password field

    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter first name"}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter last name"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "middle_name",
            "institution",
            "position",
            "date_birth",
            "sex",
            "gender",
            "specialization",
            "highest_educ",
            "contact_num",
            "user_type",
        )
        widgets = {
            "date_birth": forms.DateInput(attrs={"type": "date"}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Form for changing a user's password securely."""

    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter current password"}
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
    )


class ProfileForm(forms.ModelForm):
    """Form for updating user profile picture."""

    class Meta:
        model = Profile
        fields = ("picture",)
