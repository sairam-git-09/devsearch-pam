from django.db.models.signals import post_save, post_delete
from django.db import models
from django.contrib.auth.models import User # built in user model
from django.dispatch import receiver    
from .models import Profile 
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )    
        
        subject = "Welcome to DevSearch"
        message = "We are glad you are here"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

        profile.save()
        
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
       


@receiver(post_save, sender=Profile) 
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    

#post_save.connect(createProfile, sender=User)  # when profile is saved this function will be called
#post_delete.connect(deleteUser, sender=Profile)  # when profile is deleted this function will be called
#post_save.connect(updateUser, sender=Profile)

#post_save.connect(createProfile, sender=User) 
#post_save.connect(updateUser, sender=Profile)
#if created == False removes the possibility of infinite loop