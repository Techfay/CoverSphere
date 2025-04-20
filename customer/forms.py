from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['address', 'mobile', 'profile_pic']


class PremiumCalculationForm(forms.Form):
    # Define fields for the form
    age = forms.IntegerField(label='Age', min_value=18, max_value=100)
    coverage_amount = forms.DecimalField(label='Coverage Amount', min_value=1000, max_value=1000000, decimal_places=2)
    risk_factor = forms.ChoiceField(label='Risk Factor', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    # Method to calculate the premium based on the given data
    def calculate_premium(self):
        # Get the form's cleaned data
        age = self.cleaned_data['age']
        coverage_amount = self.cleaned_data['coverage_amount']
        risk_factor = self.cleaned_data['risk_factor']

        # Base premium (this is an arbitrary base, you can adjust it as needed)
        base_premium = 1000

        # Age-based premium factor (you can adjust these factors as per your business logic)
        if age < 25:
            age_factor = 1.2  # Younger age means higher risk
        elif age < 50:
            age_factor = 1.0  # Standard rate for middle-aged customers
        else:
            age_factor = 1.5  # Older age increases risk

        # Coverage-based premium factor (higher coverage leads to higher premiums)
        if coverage_amount < 10000:
            coverage_factor = 1.0
        elif coverage_amount < 100000:
            coverage_factor = 1.2
        else:
            coverage_factor = 1.5

        # Risk factor multiplier
        if risk_factor == 'low':
            risk_factor_multiplier = 1.0
        elif risk_factor == 'medium':
            risk_factor_multiplier = 1.2
        else:
            risk_factor_multiplier = 1.5

        # Final premium calculation
        premium = base_premium * age_factor * coverage_factor * risk_factor_multiplier
        return round(premium, 2)
