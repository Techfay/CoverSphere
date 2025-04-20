from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer



class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name

class Policy(models.Model):
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    policy_name=models.CharField(max_length=200)
    sum_assurance=models.PositiveIntegerField()
    premium=models.PositiveIntegerField()
    tenure=models.PositiveIntegerField()
    creation_date =models.DateField(auto_now=True)

    @property
    def duration_date(self):
        """Calculate the expiration date of the policy."""
        return self.creation_date + timedelta(days=self.tenure * 30)  # Approximation for months

    def is_expired(self):
        """Check if the policy is expired."""
        return date.today() > self.duration_date
    def __str__(self):
        return self.policy_name

class PolicyRecord(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy= models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_date and not self.due_date:
            self.due_date = self.start_date + timedelta(days=self.Policy.tenure * 30)
        super().save(*args, **kwargs)

    
    def auto_renew(self):
        # Only renew if policy is active and due date is reached
        if self.status == 'Approved' and self.due_date and self.due_date <= date.today():
            # Extend due date by the policy's tenure duration
            self.due_date += timedelta(days=self.Policy.tenure * 30)
            self.save()

    def __str__(self):
        return self.policy

class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description
    
class Claim(models.Model):
    CLAIM_STATUS = (
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    
    policy_record = models.ForeignKey(PolicyRecord, on_delete=models.CASCADE)
    claim_date = models.DateField(auto_now_add=True)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='Pending')
    admin_comment = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)


    payment_status = models.CharField(max_length=20, default="Unpaid")  # "Paid" or "Unpaid"
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # e.g., "Bank Transfer", "Credit Card"

class ClaimDocument(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    document = models.FileField(upload_to='claim_documents/')
    document_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
# Define the AgentProfile model
class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default-profile.png')
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        
class InsurancePolicy(models.Model):
    policy_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sum_assurance = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # Duration of the policy in months
    agent = models.ForeignKey('AgentProfile', on_delete=models.CASCADE)  # Assuming this is your agent profile model

    def __str__(self):
        return self.policy_name