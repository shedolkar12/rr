from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models hereself.

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserDetails(models.Model):
    # reg_id and facebook_id is the same
    reg_id = models.CharField(max_length=100)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    profile = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.name
    def __str__(self):
        return u'%s' % (self.name)
