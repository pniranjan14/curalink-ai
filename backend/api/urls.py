from django.urls import path
from .views import ChatView, ConversationHistoryView, HealthCheckView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('conversation/<uuid:session_id>/', ConversationHistoryView.as_view(), name='conversation-history'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
