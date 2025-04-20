from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM
from django.contrib import messages
from django.contrib.auth import logout
from .models import Claim, ClaimDocument, PolicyRecord, Customer, Policy, InsurancePolicy
from .forms import ClaimForm, ClaimDocumentForm, PaymentForm, AgentUserForm, AgentProfileForm, PolicyForm
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Policy


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'insurance/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')
    
def logout_view(request):
    logout(request)
    return redirect('/')




def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_policy':models.Policy.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_policy_holder':models.PolicyRecord.objects.all().count(),
        'approved_policy_holder':models.PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':models.PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':models.PolicyRecord.objects.all().filter(status='Pending').count(),
    }
    return render(request,'insurance/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})



@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'insurance/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  
  

def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')


def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})

def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})



def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

@login_required(login_url='adminlogin')
def update_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
  
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})
    
def delete_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')

def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_disapproved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_waiting_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def approve_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

def disapprove_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})







def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})



@login_required
def file_claim_view(request, policy_record_id):
    policy_record = get_object_or_404(PolicyRecord, id=policy_record_id)
    
    if request.method == 'POST':
        claim_form = ClaimForm(request.POST)
        document_form = ClaimDocumentForm(request.POST, request.FILES)
        
        if claim_form.is_valid() and document_form.is_valid():
            claim = claim_form.save(commit=False)
            claim.policy_record = policy_record
            claim.save()
            
            document = document_form.save(commit=False)
            document.claim = claim
            document.save()
            
            messages.success(request, 'Claim filed successfully!')
            return redirect('claim-status')
    else:
        claim_form = ClaimForm()
        document_form = ClaimDocumentForm()
    
    return render(request, 'customer/file_claim.html', {
        'claim_form': claim_form,
        'document_form': document_form,
        'policy_record': policy_record
    })

@login_required
def claim_status_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    claims = Claim.objects.filter(
        policy_record__customer=customer
    ).order_by('-claim_date')
    
    return render(request, 'customer/claim_status.html', {'claims': claims})

# Admin Views
@login_required
@user_passes_test(lambda u: not u.groups.filter(name='CUSTOMER').exists())
def admin_claims_view(request):
    claims = Claim.objects.all().order_by('-claim_date')
    return render(request, 'insurance/admin_claims.html', {'claims': claims})

@login_required
@user_passes_test(lambda u: not u.groups.filter(name='CUSTOMER').exists())
def process_claim_view(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        comment = request.POST.get('admin_comment')
        
        claim.status = status
        claim.admin_comment = comment
        claim.save()
        
        messages.success(request, 'Claim updated successfully!')
        return redirect('admin-claims')
    
    return render(request, 'insurance/process_claim.html', {'claim': claim})


def process_claim_payment_view(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)

    if claim.status != "Approved":
        return redirect('admin-claims')  # Redirect if the claim is not approved

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Update claim payment details
            claim.payment_status = "Paid"
            claim.payment_date = timezone.now()
            claim.payment_method = form.cleaned_data['payment_method']
            claim.save()

            # You can add code here to generate and save a payment receipt

            return redirect('admin-claims')  # Redirect after payment
    else:
        form = PaymentForm()

    context = {
        'claim': claim,
        'form': form,
    }
    return render(request, 'insurance/claim_payment_form.html', context)


def generate_payment_receipt(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)

    # Define the path where the receipt will be saved
    receipts_dir = os.path.join(settings.BASE_DIR, 'static', 'receipts')
    
    # Ensure the receipts directory exists
    if not os.path.exists(receipts_dir):
        os.makedirs(receipts_dir)
    
    # Create the receipt file path
    receipt_filename = f'receipt_{claim_id}.pdf'
    receipt_filepath = os.path.join(receipts_dir, receipt_filename)

    # Create the PDF and save it to the specified path
    p = canvas.Canvas(receipt_filepath)
    p.drawString(100, 800, f"Payment Receipt for Claim {claim.id}")
    p.drawString(100, 780, f"Customer: {claim.policy_record.customer.get_name()}")
    p.drawString(100, 760, f"Policy: {claim.policy_record.Policy.policy_name}")
    p.drawString(100, 740, f"Amount Paid: ${claim.claim_amount}")
    p.drawString(100, 720, f"Payment Date: {claim.payment_date}")
    p.drawString(100, 700, f"Payment Method: {claim.payment_method}")
    p.showPage()
    p.save()

    # Provide the file path for download
    return HttpResponse(f'Receipt saved! You can download it from <a href="/static/receipts/{receipt_filename}">here</a>.')



@csrf_exempt
def apply_policy_view(request, policy_id):
    if request.method == 'POST':
        try:
            # Get the policy and customer
            policy = get_object_or_404(Policy, id=policy_id)
            customer = get_object_or_404(Customer, user=request.user)
            
            # Get start date from the form
            start_date = request.POST.get('start_date')
            if not start_date:
                return JsonResponse({
                    'success': False,
                    'message': 'Start date is required'
                })
            
            # Convert string to date object
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            # Calculate due date based on policy tenure
            due_date = start_date + timedelta(days=policy.tenure * 30)
            
            # Create policy record
            policy_record = PolicyRecord.objects.create(
                customer=customer,
                Policy=policy,
                start_date=start_date,
                due_date=due_date,
                status='Pending'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Policy application submitted successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })



def renew_policy_view(request, policy_record_id):
    policy_record = get_object_or_404(PolicyRecord, id=policy_record_id)

    # Ensure the policy can be renewed
    if policy_record.due_date and policy_record.due_date <= timezone.now().date():
        policy_record.due_date += timedelta(days=policy_record.Policy.tenure * 30)
        policy_record.save()
        messages.success(request, "Policy renewed successfully.")
    else:
        messages.error(request, "Policy cannot be renewed at this time.")
    
    return redirect('history')


def admin_renew_policy_status_view(request):
    today = timezone.now().date()
    renewal_policies = PolicyRecord.objects.filter(due_date__lte=today, status='Approved')

    context = {
        'renewal_policies': renewal_policies,
    }
    return render(request, 'insurance/admin_renew_policy_status.html', context)

def renew_policy_view(request, policy_id):
    policy = get_object_or_404(PolicyRecord, id=policy_id)
    
    # Renew policy by updating due date
    if policy.due_date <= timezone.now().date():
        policy.start_date = timezone.now().date()
        policy.due_date = policy.start_date + timedelta(days=policy.Policy.tenure * 30)
        policy.save()
    return redirect('admin-renew-policy-status')
    
    
def health_insurance(request):
    return render(request, 'insurance/health_insurance.html')
    
def life_insurance(request):
    return render(request, 'insurance/life_insurance.html')
    
def auto_insurance(request):
    return render(request, 'insurance/auto_insurance.html')
    
def home_insurance(request):
    return render(request, 'insurance/home_insurance.html')
    
def agent_signup_view(request):
    user_form = AgentUserForm()
    profile_form = AgentProfileForm()
    
    if request.method == 'POST':
        user_form = AgentUserForm(request.POST)
        profile_form = AgentProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            agent_profile = profile_form.save(commit=False)
            agent_profile.user = user
            agent_profile.save()
            
            agent_group = Group.objects.get_or_create(name='AGENT')
            agent_group[0].user_set.add(user)
            
            return redirect('agent-login')  # Redirect after successful signup
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'insurance/agent_signup.html', context)
    
def agent_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.groups.filter(name='AGENT').exists():
                login(request, user)
                return redirect('agent-dashboard')
            else:
                messages.error(request, 'Invalid credentials or you do not have agent privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'insurance/agent_login.html', {'form': form})
    


@login_required(login_url='agent-login')
def agent_dashboard_view(request):
    # Fetch the agent's profile
    agent_profile = request.user.agentprofile

    # Fetch all policies to be displayed on the agent's dashboard
    all_policies = Policy.objects.all()

    # Performance Metrics (Placeholder examples)
    total_policies_sold = 0  # This would be updated with actual logic
    total_claims_processed = 0  # This would be updated with actual logic
    total_clients_managed = 0  # This would be updated with actual logic
    current_commission_earned = 0.0  # This would be updated with actual logic

    context = {
        'agent_name': request.user.get_full_name(),
        'agent_profile': agent_profile,
        'all_policies': all_policies,
        'total_policies_sold': total_policies_sold,
        'total_claims_processed': total_claims_processed,
        'total_clients_managed': total_clients_managed,
        'current_commission_earned': current_commission_earned,
    }
    return render(request, 'insurance/agent_dashboard.html', context)

    
@login_required(login_url='agent-login')
def edit_policy_view(request, pk):
    policy = get_object_or_404(Policy, pk=pk)

    if request.method == 'POST':
        policy_form = PolicyForm(request.POST, instance=policy)
        if policy_form.is_valid():
            policy_form.save()
            messages.success(request, "Policy updated successfully.")
            return redirect('agent-dashboard')
        else:
            messages.error(request, "Failed to update policy. Please check the form for errors.")
    else:
        policy_form = PolicyForm(instance=policy)

    context = {
        'policy_form': policy_form,
        'policy': policy
    }

    return render(request, 'insurance/edit_policy.html', context)
    
@login_required(login_url='agent-login')
def delete_policy_view(request, pk):
    policy = get_object_or_404(Policy, pk=pk)

    if request.method == 'POST':
        policy.delete()
        messages.success(request, "Policy deleted successfully.")
        return redirect('agent-dashboard')

    return render(request, 'insurance/delete_policy_confirm.html', {'policy': policy})