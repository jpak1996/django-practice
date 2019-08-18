from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

# source code for both abstract classes:
# https://github.com/django/django/blob/master/django/contrib/auth/base_user.py

# default user model:
# https://docs.djangoproject.com/en/2.2/ref/contrib/auth/

# customized example:
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#django.contrib.auth.models.CustomUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length= 254,
        unique = True,
    )
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.DateField
    # this should get current time whenever new user is created
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # last_login field should already exist in AbstractBaseUser

    # @property
    # def is_staff(self):
    #     return self.is_superuser # set all superusers as staff for now
    """
    TODO: define permissions
    
    def has_perm(self, perm, obj=None):
        return True
    """
