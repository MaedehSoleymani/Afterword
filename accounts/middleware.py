from django.utils import timezone
from .models import C_User

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last = request.user.last_activity
            if not last or (now - last).total_seconds() > 60:
                C_User.objects.filter(pk=request.user.pk).update(
                    last_activity=now
                )
        return self.get_response(request)