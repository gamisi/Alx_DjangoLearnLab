from django.db import models
# from posts.models import Post
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser

# Create your models here.
class Notification(models.Model):
    recipient = models.CharField(max_length=100)
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_sent')
    verb = models.CharField(max_length=100)

    # This sets up a generic relationship so we can link to any object (like a Post)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Content type of the target object (Post, Comment, etc.)
    target_object_id = models.PositiveIntegerField()  # get the ID of the target object
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.actor.username} {self.verb} {self.target}"

    # Latest notifications first
    class Meta:
        ordering = ['-timestamp']  