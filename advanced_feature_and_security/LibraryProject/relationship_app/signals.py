from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Create or update the UserProfile when a User is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile when a new user is created
        UserProfile.objects.create(user=instance)
    else:
        # Save the UserProfile when an existing user is updated
        instance.profile.save()
