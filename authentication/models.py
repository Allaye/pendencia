from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from helpers.models import TrackingModel
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (PermissionsMixin, UserManager, AbstractBaseUser)
from helpers.models import TrackingModel


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email and passsword
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, username: str, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username: str, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(username, email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=150, unique=True, help_text='Required, 150 characters or fewer', error_messages={'unique':'a User with this user name is already registered'}, validators=[username_validator])
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text='Designated user can login using this account')
    is_active = models.BooleanField(_('active'), default=True, help_text='Designated whether this user should be treated as active')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(_('email_verified'), default=False,)
    objects = MyUserManager()

    EMAIL_FIELD = 'email'  
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        token = jwt.encode({
            'username': self.username, 
            'email': self.email, 
            'exp': datetime.utcnow()+ timedelta(hours=24)}, 
            settings.SECRET_KEY, algorithm='HS256')
        return token