from datetime import datetime
from django.http import HttpResponseForbidden
import logging
import pytz  # optional, but preferred
from django.http import JsonResponse
from collections import defaultdict
from django.http import HttpResponseForbidden


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
    

class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST requests (messages) per IP.
    Limit: 5 messages per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store IP access times
        self.ip_requests = defaultdict(list)

    def __call__(self, request):
        # Only limit POST requests (assuming messages are sent via POST)
        if request.method == "POST":
            ip = self.get_ip(request)
            now = time.time()

            # Filter timestamps older than 60 seconds
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if now - t < 60]

            if len(self.ip_requests[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            # Add current timestamp
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_ip(self, request):
        """Retrieve IP address of the client."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow superusers or moderators
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")

        # Assuming your User model has a 'role' attribute
        if hasattr(user, 'role') and user.role.lower() not in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response