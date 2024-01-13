from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountMnager(BaseUserManager):
    # creating for normal user
    def create_user(self, f_name, l_name, username, email, password=None):
        if not email:
            raise ValueError('please enter email')
        
        if not username:
            raise ValueError('please enter username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            f_name = f_name,
            l_name = l_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #creating for super user
    def create_superuser(self, username, l_name, f_name, password, email):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            f_name = f_name,
            l_name = l_name,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(unique=True, max_length=200)
    ph_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'f_name', 'l_name'] 


    objects = MyAccountMnager()


    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True