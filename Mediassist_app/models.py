from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Login_view(AbstractUser):
    is_users = models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)


class users(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()

    trust_register_number = models.CharField(max_length=16)
    profile_pic = models.FileField(upload_to='profilepic/')
    verified = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class donor(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE, related_name='donor')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    reg_no = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Medicine_request(models.Model):
    CHOICE = [
        ('1-2 months', '1-2 months'),
        ('6 months', '6 months'),
        ('1 year', '1 year'),

    ]
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    end_date = models.CharField(max_length=25)
    medicine_name = models.CharField(max_length=50)
    prescription = models.FileField(upload_to='pic/')
    quantity = models.CharField(max_length=50, choices=CHOICE)
    status_1 = models.IntegerField(default=0)


class Medicine_approval(models.Model):
    user = models.ForeignKey(donor, on_delete=models.CASCADE)
    approval = models.ForeignKey(Medicine_request, on_delete=models.CASCADE, related_name='approval')
    status1 = models.IntegerField(default=0)
    status2 = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    note = models.CharField(max_length=200, null=True, blank=True)


class Cash_request(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()
    description = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    status_12 = models.IntegerField(default=0)


#
class Cash_approval(models.Model):
    user = models.ForeignKey(donor, on_delete=models.CASCADE)
    approval = models.ForeignKey(Cash_request, on_delete=models.CASCADE)
    status1 = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    paystat = models.IntegerField(default=0)


class payment(models.Model):
    user = models.ForeignKey(Cash_approval, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    exp = models.DateField()
    cvv = models.CharField(max_length=3)


# feedbacks and reply
class Feedback(models.Model):
    user = models.ForeignKey(Login_view, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    date = models.DateField(auto_now=True)
    reply = models.TextField(null=True, blank=True)
