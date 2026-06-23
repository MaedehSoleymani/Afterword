#ACCOUNT MODELS
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
import secrets

class C_UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_author", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)
            
class C_User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True, null=False, blank=False)
    date_joined=models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_active=models.BooleanField(default=True, null=False, blank=False)
    is_superuser=models.BooleanField(default=False, null=False, blank=False)
    is_author=models.BooleanField(default=False, null=False, blank=False)
    is_staff=models.BooleanField(default=False, null=False, blank=False)  # ← ADD THIS

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = C_UserManager()

    def __str__(self):
        return self.email

class UserToken(models.Model):
    TOKEN_TYPES=[
        ('verify_email','Verify Email'),
        ('change_email','Change Email'),
        ('reset_password','Reset Password')
    ]

    user=models.ForeignKey(C_User, on_delete=models.CASCADE)
    token=models.CharField(max_length=100, null=False, unique=True)
    token_type=models.CharField(max_length=20, null=False, choices=TOKEN_TYPES)
    created_at=models.DateTimeField(auto_now_add=True, null=False)
    expires_at=models.DateTimeField(null=False)
    is_used=models.BooleanField(default=False, null=False)
    pending_email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(48)
        if not self.expires_at:
            if self.token_type == 'reset_password':
                self.expires_at = timezone.now() + timezone.timedelta(hours=1)
            else:
                self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"{self.user.email} - {self.token_type} - {self.is_valid()}"
