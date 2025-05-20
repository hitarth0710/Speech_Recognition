# app/routes/main.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models.recording import Recording

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page route"""
    return render_template('index.html', user=current_user)


@main_bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    # Get recent recordings for the current user
    recent_recordings = Recording.query.filter_by(user_id=current_user.id) \
        .order_by(Recording.timestamp.desc()) \
        .limit(5) \
        .all()

    return render_template('dashboard/index.html',
                           user=current_user,
                           recordings=recent_recordings)


@main_bp.route('/history')
@login_required
def history():
    """Speech recognition history route"""
    # Get all recordings for the current user
    recordings = Recording.query.filter_by(user_id=current_user.id) \
        .order_by(Recording.timestamp.desc()) \
        .all()

    return render_template('dashboard/history.html', recordings=recordings)

@main_bp.route('/recording/<int:recording_id>')
@login_required
def view_recording(recording_id):
    recording = Recording.query.get_or_404(recording_id)
    
    # Ensure the user can only access their own recordings
    if recording.user_id != current_user.id:
        flash('You do not have permission to view this recording', 'danger')
        return redirect(url_for('main.history'))
    
    return render_template('dashboard/view_recording.html', recording=recording)