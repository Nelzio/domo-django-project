from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_resetpassword.signals import reset_password_token_created
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_user_name, last_user_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_user_name=first_user_name,
            last_user_name=last_user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_user_name, last_user_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_user_name=first_user_name,
            last_user_name=last_user_name
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    telephone = models.CharField(
        max_length=9, null=True, blank=True, unique=True)
    first_user_name = models.CharField(max_length=255)
    last_user_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_user_name', 'last_user_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.staff

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin

    @property
    def first_name(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.first_user_name

    @property
    def last_name(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.last_user_name


class Code(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
