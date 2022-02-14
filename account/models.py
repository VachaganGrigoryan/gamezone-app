from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from account.manager import UserManager, SignUpCodeManager, PasswordResetCodeManager, EmailChangeCodeManager
from core.mail import send_multi_format_email


class User(AbstractBaseUser, PermissionsMixin):
    guid = models.UUIDField(auto_created=True, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this user is verified the email address.'
        )
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('account:account-detail', kwargs={'guid': self.guid})


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(_('Avatar'), upload_to="profiles/avatars/", null=True, blank=True)
    banner = models.ImageField(_('Banner'), upload_to="profiles/banners/", null=True, blank=True)

    bio = models.TextField(_('About'), blank=True)
    address = models.CharField(_('Address'), blank=True, max_length=250)
    country = models.CharField(_('Country'), blank=True, max_length=100)
    region = models.CharField(_('State/Region'), blank=True, max_length=100)
    city = models.CharField(_('City'), blank=True, max_length=50)
    zip_code = models.CharField(_('Zip/Code'), blank=True, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class AbcBaseCode(models.Model):
    EXPIRY_PERIOD = 3

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_mail(self, prefix):
        context = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': self.code
        }
        send_multi_format_email(prefix, context, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignUpCode(AbcBaseCode):
    objects = SignUpCodeManager()

    class Meta:
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Codes'

    def send_signup_mail(self):
        self.send_mail(prefix='signup_email')


class PasswordResetCode(AbcBaseCode):
    objects = PasswordResetCodeManager()

    class Meta:
        verbose_name = 'Password Reset Code'
        verbose_name_plural = 'Password Reset Codes'

    def send_password_reset_email(self):
        self.send_mail(prefix='password_reset_email')


class EmailChangeCode(AbcBaseCode):
    email = models.EmailField(max_length=255)

    objects = EmailChangeCodeManager()

    class Meta:
        verbose_name = 'Email Change Code'
        verbose_name_plural = 'Email Change Codes'

    def send_email_change_email(self):
        self.send_mail(prefix='email_change_notify_previous_email')

        prefix = 'email_change_confirm_new_email'
        context = {
            'email': self.email,
            'code': self.code
        }
        send_multi_format_email(prefix, context, target_email=self.email)
