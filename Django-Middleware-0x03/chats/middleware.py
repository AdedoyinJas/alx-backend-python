from datetime import datetime
from django.http import HttpResponseForbidden
import logging
import pytz  # optional, but preferred

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Configure logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        
        logging.info(log_entry)

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (UTC or your timezone)
        now = datetime.now()

        # Extract hour
        current_hour = now.hour

        # Allowed: from 6AM (06) to 9PM (21)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat access restricted at this time.")

        return self.get_response(request)
