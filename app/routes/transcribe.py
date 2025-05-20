from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import pytz
from flask_login import login_required, current_user

from app.services.speech_recognition import transcribe_audio
from app.utils.validators import allowed_file
from app.models.recording import Recording
from app import db

transcribe_bp = Blueprint('transcribe', __name__, url_prefix='/transcribe')

class SimpleRecording:
    """Temporary recording object for demo mode when not using database"""
    def __init__(self, filename, original_filename=None, transcription=None, display_name=None):
        self.id = str(uuid.uuid4())
        self.filename = filename
        self.original_filename = original_filename or filename
        self.transcription = transcription
        self.display_name = display_name or original_filename
        self.text = transcription  # For compatibility
        self.created_at = datetime.now(pytz.utc)
        self.timestamp = datetime.now(pytz.utc)

@transcribe_bp.route('/', methods=['GET'])
def index():
    """Display the transcription page"""
    return render_template('transcribe/index.html')

# Update the upload_file function to handle custom name

@transcribe_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and transcription"""
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    
    # Get custom name if provided
    custom_name = request.form.get('custom_name', '').strip()
    
    if file and allowed_file(file.filename):
        # Generate a secure filename to prevent path traversal attacks
        original_filename = secure_filename(file.filename)
        # Generate a unique ID for the file
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        
        # Make sure the upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file to the upload folder
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        # Transcribe the audio file
        try:
            # Process audio with speech recognition
            transcription = transcribe_audio(filepath)
            
            # If user is logged in, store in database
            if current_user.is_authenticated:
                # Create a database recording with custom name if provided
                recording = Recording(
                    filename=unique_filename,
                    text=transcription,
                    user_id=current_user.id,
                    file_size=os.path.getsize(filepath),
                    original_filename=original_filename,
                    display_name=custom_name if custom_name else original_filename
                )
                db.session.add(recording)
                db.session.commit()
                
                flash('Audio transcription completed successfully!', 'success')
                return render_template('transcribe/result.html', recording=recording)
            else:
                # For demonstration, use a simple object without database
                recording = SimpleRecording(
                    filename=unique_filename,
                    original_filename=original_filename,
                    transcription=transcription,
                    display_name=custom_name if custom_name else original_filename
                )
                
                return render_template('transcribe/result.html', recording=recording)
                
        except Exception as e:
            current_app.logger.error(f'Error transcribing audio: {str(e)}')
            flash(f'Error transcribing audio: {str(e)}', 'danger')
            return redirect(request.url)
    
    flash('File type not allowed', 'danger')
    return redirect(request.url)

@transcribe_bp.route('/files/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@transcribe_bp.route('/result/<int:recording_id>')
@login_required
def result(recording_id):
    """Display the transcription result for a specific recording"""
    recording = Recording.query.get_or_404(recording_id)
    
    # Ensure the user can only access their own recordings
    if recording.user_id != current_user.id:
        flash('You do not have permission to view this recording', 'danger')
        return redirect(url_for('main.history'))
    
    return render_template('transcribe/result.html', recording=recording)