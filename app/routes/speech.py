import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

# Import both functions to ensure compatibility with existing code
from app.services.speech_recognition import recognize_speech, transcribe_audio
from app.models.recording import Recording
from app.utils.validators import allowed_file
from app import db

speech_bp = Blueprint('speech', __name__, url_prefix='/speech')

@speech_bp.route('/', methods=['GET'])
def index():
    """Display the speech recognition page"""
    return render_template('speech/index.html')

@speech_bp.route('/upload', methods=['POST'])
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
            # Process audio with speech recognition (using either the new or old method)
            transcription = transcribe_audio(filepath)
            
            # If user is logged in, store in database
            if current_user.is_authenticated:
                # Create a database recording
                recording = Recording(
                    filename=unique_filename,
                    text=transcription,  # Use text for backward compatibility
                    transcription=transcription,  # Use transcription for new implementations
                    user_id=current_user.id,
                    file_size=os.path.getsize(filepath),
                    original_filename=original_filename
                )
                db.session.add(recording)
                db.session.commit()
                
                flash('Audio transcription completed successfully!', 'success')
                return render_template('speech/result.html', recording=recording)
            else:
                # For demonstration without login
                class SimpleRecording:
                    """Temporary recording object for demo mode when not using database"""
                    def __init__(self, filename, original_filename=None, transcription=None):
                        self.id = str(uuid.uuid4())
                        self.filename = filename
                        self.original_filename = original_filename or filename
                        self.transcription = transcription
                        
                recording = SimpleRecording(
                    filename=unique_filename,
                    original_filename=original_filename,
                    transcription=transcription
                )
                
                return render_template('speech/result.html', recording=recording)
                
        except Exception as e:
            current_app.logger.error(f'Error transcribing audio: {str(e)}')
            flash(f'Error transcribing audio: {str(e)}', 'danger')
            return redirect(request.url)
    
    flash('File type not allowed', 'danger')
    return redirect(request.url)

@speech_bp.route('/files/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)