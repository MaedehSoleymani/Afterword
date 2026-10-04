from django.urls import path, include
from API_app.views import MessageListView

urlpatterns=[
    path ('get/messages', MessageListView.as_view(), name='get_messages')
]