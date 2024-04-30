from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class AccountManager(BaseUserManager):

     def create_user(self, first_name, last_name,username,phone, email,password=None):

       user = self.model(
           email=self.normalize_email(email),
           first_name=first_name,
           last_name=last_name,
           username=username,
           phone=phone
            )
       user.is_admin = False
       user.is_superuser = False
       user.is_staff = False
       user.is_active = True
       user.set_password(password)
       user.save(using=self._db)
       return user

     def create_superuser(self, first_name, last_name,username,phone, email,password=None):

       user = self.model(
           email=self.normalize_email(email),
           first_name=first_name,
           last_name=last_name,
           username=username,
           phone=phone
            )
       user.is_admin = True
       user.is_superuser = True
       user.is_staff = True
       user.is_active = True
       user.set_password(password)
       user.save(using=self._db)
       return user


class BillingAddress(models.Model):
    billing_address_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.UUIDField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PaymentMethod(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    card_type = models.CharField(max_length=50)
    card_last_four = models.CharField(max_length=4)
    expiration_date = models.CharField(max_length=10)


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,blank=True)
    username = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=100,unique=True)
    email = models.CharField(max_length=100,unique=True)

    registered_on = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    PaymentMethods = models.ManyToManyField(PaymentMethod, related_name='accounts')
    BillingAddresses = models.ManyToManyField(BillingAddress, related_name='accounts')
    primaryAddress = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True,blank=True,  related_name='primary_account')
    primaryPaymentOption = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True, related_name='primary_account')
    #registration_ip = models.CharField(max_length=100,blank=False)
    #last_login_ip = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name','username','phone']
    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser




