# app/utils/security.py
import secrets
from functools import wraps
from flask import abort, current_app, request
from flask_login import current_user


def generate_secure_token(length=32):
    """Generate a secure random token with the given length."""
    return secrets.token_hex(length // 2)


def validate_secure_token(token):
    """Validate if a token meets security requirements.

    Args:
        token (str): The token to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Check if token is at least 16 characters long
    if not token or len(token) < 16:
        return False

    # Additional validation can be added here
    return True


def admin_required(func):
    """Decorator to require admin role for a route."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


def csrf_protect(func):
    """Basic CSRF protection decorator."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Only apply to POST, PUT, PATCH, DELETE methods
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            token = request.form.get('_csrf_token')
            if not token or token != session.get('_csrf_token'):
                abort(403)
        return func(*args, **kwargs)

    return decorated_view


def rate_limit(func=None, limit=5, period=60):
    """
    Rate limiting decorator.

    Args:
        func: The function to decorate
        limit (int): Number of allowed requests per period
        period (int): Time period in seconds

    Returns:
        function: The decorated function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get identifier (IP or user ID if logged in)
            if current_user.is_authenticated:
                identifier = str(current_user.id)
            else:
                identifier = request.remote_addr

            # Simple in-memory rate limiting (in production, use Redis or similar)
            cache_key = f"ratelimit:{identifier}:{request.endpoint}"

            # Placeholder for actual rate limiting implementation
            # In a real application, you'd use Redis or a similar tool

            return f(*args, **kwargs)

        return decorated_function

    if func:
        return decorator(func)
    return decorator