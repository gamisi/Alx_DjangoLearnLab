from django.urls import path, include
from .views import create_notification
from .import views
urlpatterns = [

    path('notifications/', views.NotificationListView.as_view(), name='notifications'),

]