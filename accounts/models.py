from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class hello(BaseUserManager):   #this is second  
#create user   
# go to https://docs.djangoproject.com/en/4.1/topics/auth/customizing/ for detail information
    def create_user(self,first_name,last_name,username,email,phone_number,password=None):   #password always be none
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        #thanks to Django documentary
    #write function for creating super user
    def create_superuser(self,email,first_name,last_name,username,phone_number,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        #once all these done, give permission for superadmin
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):    # this is first, do this function first
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    email=models.EmailField(max_length=200,unique=True)
    phone_number=models.IntegerField()
    #mandatory
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    #link Account and hello
    objects=hello()

    #login field
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username','phone_number']

    def __str__(self):
        return self.email

    #mandatory
    def has_perm(self,perm,obj=None):
        return self.is_admin    #this mean if the user is admin, he/she has the permission to access all things and do any changes
    
    def has_module_perms(self,add_label):
        return True
    