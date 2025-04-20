from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from .forms import PremiumCalculationForm
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('/')

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'customer/customerclick.html')

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            return redirect('customer-login')  # Redirect to the customer login page after successful signup
    return render(request, 'customer/customersignup.html', context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    dict = {
        'customer': customer,
        'available_policy': CMODEL.Policy.objects.all().count(),
        'applied_policy': CMODEL.PolicyRecord.objects.all().filter(customer=customer).count(),
        'total_category': CMODEL.Category.objects.all().count(),
        'total_question': CMODEL.Question.objects.all().filter(customer=customer).count(),
    }
    return render(request, 'customer/customer_dashboard.html', context=dict)

@login_required(login_url='customerlogin')
def apply_policy_view(request):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    policies = CMODEL.Policy.objects.all()
    return render(request, 'customer/apply_policy.html', {'policies': policies, 'customer': customer})

@login_required(login_url='customerlogin')
def apply_view(request, pk):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

@login_required(login_url='customerlogin')
def history_view(request):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    return render(request, 'customer/history.html', {'policies': policies, 'customer': customer})

@login_required(login_url='customerlogin')
def ask_question_view(request):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    questionForm = CFORM.QuestionForm()
    
    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect('question-history')
    return render(request, 'customer/ask_question.html', {'questionForm': questionForm, 'customer': customer})

@login_required(login_url='customerlogin')
def question_history_view(request):
    try:
        customer = models.Customer.objects.get(user_id=request.user.id)
    except models.Customer.DoesNotExist:
        return redirect('customer_signup')  # Redirect to signup if Customer profile does not exist
    
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request, 'customer/question_history.html', {'questions': questions, 'customer': customer})

def premium_calculation_view(request):
    premium = None  # Default value, will be updated if the form is submitted and valid
    if request.method == 'POST':
        form = PremiumCalculationForm(request.POST)
        if form.is_valid():
            # Calculate premium based on form data
            premium = form.calculate_premium()
    else:
        form = PremiumCalculationForm()

    # Render the template and pass the form and premium data
    return render(request, 'customer/premium_calculation.html', {'form': form, 'premium': premium})

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            return redirect('customer-login')
    mydict['login_link'] = True  # Add a flag to show the login link on the signup page
    return render(request, 'customer/customersignup.html', context=mydict)
