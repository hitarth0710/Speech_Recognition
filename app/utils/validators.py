# app/utils/validators.py
import re
import os

def allowed_file(filename):
    """
    Check if a file has an allowed extension
    
    Args:
        filename: The name of the file to check
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Original function for backward compatibility
def allowed_audio_file(filename):
    """
    Check if the uploaded file is an allowed audio format
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return allowed_file(filename)

# Keep the rest of the validators.py content
def validate_registration(username, email, password, confirm_password=None):
    """
    Validate user registration data

    Args:
        username (str): Username to validate
        email (str): Email to validate
        password (str): Password to validate
        confirm_password (str, optional): Password confirmation

    Returns:
        str or None: Error message if validation fails, None otherwise
    """
    # Validate username
    if not username or len(username) < 3:
        return "Username must be at least 3 characters long"

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Username can only contain letters, numbers, and underscores"

    # Validate email
    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Please enter a valid email address"

    # Validate password
    if not password or len(password) < 8:
        return "Password must be at least 8 characters long"

    # Check password complexity
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password):
        return "Password must contain at least one uppercase letter, one lowercase letter, and one number"

    # Check if passwords match
    if confirm_password is not None and password != confirm_password:
        return "Passwords do not match"

    return None


def validate_login(username, password):
    """
    Validate login data

    Args:
        username (str): Username to validate
        password (str): Password to validate

    Returns:
        str or None: Error message if validation fails, None otherwise
    """
    if not username:
        return "Please enter a username"

    if not password:
        return "Please enter a password"

    return None


def validate_audio_recording(file_path, max_size_mb=10):
    """
    Validate an audio recording file

    Args:
        file_path (str): Path to the audio file
        max_size_mb (int): Maximum allowed file size in MB

    Returns:
        str or None: Error message if validation fails, None otherwise
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return "Audio file does not exist"

    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return f"Audio file too large (max {max_size_mb}MB)"

    # Additional validations could be added here

    return None