from django.shortcuts import render
from .models import Notification
from posts.models import Post
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser

# Create your views here.

# Helper function to create a notification
def create_notification(actor, recipient, verb, target):
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=target.id
    )
    return notification


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')

        # Create a response with notifications and their read status
        notification_data = []
        for notification in notifications:            
            #target_str = str(notification.target)

            # Handle the case where the target is a user (i.e., follower or followed user)
            # if isinstance(notification.target, CustomUser):
                #target_str = notification.target.username  # Get the username if the target is a user

            notification_data.append({

                'actor': notification.actor.username,
                'verb': notification.verb,
                'target': str(notification.target),
                'timestamp': notification.timestamp,
                # 'is_read': notification.is_read

            })

        return Response({'notifications': notification_data}, status=200)

class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        user = request.user
        try:
            notification = Notification.objects.get(id=notification_id, recipient=user)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found'}, status=404)

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        return Response({'detail': 'Notification marked as read'}, status=200)