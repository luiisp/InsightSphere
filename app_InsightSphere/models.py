from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

class AnonymousUser(AbstractUser):
    apelido = models.CharField(max_length=16, blank=True, null=True)

class User(AbstractUser):
    apelido = models.CharField(max_length=16, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set'  
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set'  
    )

    def __str__(self):
        return self.username

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False, help_text="Este canal é verificado?")

    def __str__(self):
        return self.name

