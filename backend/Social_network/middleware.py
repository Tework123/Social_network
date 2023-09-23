import datetime

from django.utils import timezone


class FilterIPMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        try:
            user = request.user
            if user.date_last_visit < timezone.now() - datetime.timedelta(minutes=5):
                user.date_last_visit = timezone.now()
                user.save()
        except:
            pass
        return response
