import uuid

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone

from core.utils import generate_code


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        now = timezone.now()
        extra_fields.setdefault('last_login', now)
        extra_fields.setdefault('date_joined', now)
        extra_fields.setdefault('guid', uuid.uuid4())

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def all_users(self):
        return self.all().filter(is_superuser=False)


class SignUpCodeManager(models.Manager):
    def create_signup_code(self, user, ip_address):
        code = generate_code()
        signup_code = self.create(
            user=user,
            code=code,
            ip_address=ip_address
        )
        return signup_code

    def set_user_is_verified(self, code):

        signup_code = self.get_queryset().filter(code=code).first()
        if signup_code:
            signup_code.user.is_verified = True
            signup_code.user.save()

        return bool(signup_code)


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = generate_code()
        password_reset_code = self.create(
            user=user,
            code=code
        )
        return password_reset_code


class EmailChangeCodeManager(models.Manager):
    def create_email_change_code(self, user, email):
        code = generate_code()
        email_change_code = self.create(
            user=user,
            code=code,
            email=email
        )

        return email_change_code
