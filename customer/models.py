from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Customer/',null=True,blank=True,default='profile_pic/Customer/default.jpg')
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],null=False)

   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
        

