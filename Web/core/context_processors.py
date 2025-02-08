# Web/core/context_processors.py
from .models import Notification


def notification_count(request):
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(
            user=request.user, read_status=False
        ).count()
    else:
        notification_count = 0
    return {"notification_count": notification_count}
