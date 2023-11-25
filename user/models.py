
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from .manager import UserManager



class User(AbstractUser):

    username = models.CharField(
        _("username"),
        unique=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        help_text=_("Not required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"unique": _("A user with that username already exists."),},
        null=True, blank=True
    )
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=300)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    first_name = None 
    last_name = None
    groups = None
    user_permissions = None
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.email})".strip()