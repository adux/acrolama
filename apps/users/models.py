from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

PRONOUN = [("NN", "None"), ("Mr.", "Mr"), ("Ms.", "Ms"), ("Mx.", "Mx")]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_teacher", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_teacher", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_teacher") is not True:
            raise ValueError("Superuser must have is_teacher=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Important
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_teacher = models.BooleanField(_("teacher status"), default=False)
    # For all
    pronoun = models.CharField(choices=PRONOUN, max_length=10, blank=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey("address.Address", null=True, blank=True, on_delete=models.CASCADE)
    birth_date = models.DateField(_("Birthday"), null=True, blank=True)
    # Teachers and Stuff can use this
    title = models.CharField(_("title"), max_length=45, blank=True)
    avatar = models.ForeignKey("audiovisual.Avatar", blank=True, null=True, on_delete=models.CASCADE)
    short_description = models.TextField(_("short description"), max_length=400, blank=True)
    long_description = models.TextField(_("long description"), max_length=1200, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s " % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
