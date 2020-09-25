from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    """A custom manager to deal with emails as unique identifer."""
    def _create_user(self, email, password, **extra_fields):
        """Creates and save a user with a given email and password"""
        if not email:
            raise ValueError("The email must be set!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=Ture")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_("Degisnates whether the user can log in this site")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Deginates whether this user should be treated as active. Unselect this instead of deleting accounts.")
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    fullname = models.CharField(max_length=264, blank=True)
    address_1 = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}'s profile".format(self.user)
    
    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_field()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value =='':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()