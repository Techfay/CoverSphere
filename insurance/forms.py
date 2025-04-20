from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Claim, ClaimDocument
from .models import AgentProfile



class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields=['category_name']

class PolicyForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=models.Category.objects.all(),empty_label="Category Name", to_field_name="id")
    class Meta:
        model=models.Policy
        fields=['policy_name','sum_assurance','premium','tenure']

class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Question
        fields=['description']
        widgets = {
        'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_amount', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class ClaimDocumentForm(forms.ModelForm):
    class Meta:
        model = ClaimDocument
        fields = ['document', 'document_type']

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Mobile Payment', 'Mobile Payment'),
    ])
    
    
class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = ['mobile', 'address', 'profile_pic', 'is_active', 'email']
# Form to handle user-related information for the agent
class AgentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }