from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import AdvUser

@receiver(post_save,sender=AbstractUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        AdvUser.objects.create(user=instance)
