from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.



class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    phone_number=PhoneNumberField(blank=True,null=True)
    
    
    def __str__(self):
        return self.user.email
    
    
    


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    Create a new account for the user whenever a new user is created.
    """
    if created:
        Account.objects.create(user=instance)
