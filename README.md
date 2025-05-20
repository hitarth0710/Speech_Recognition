# SpeechAI - Advanced Speech Recognition Web Application

SpeechAI is a powerful web application that transforms audio recordings into accurate text transcriptions using cutting-edge AI technology. Built with Flask, Bootstrap, and the Wav2Vec 2.0 speech recognition model, this application offers a seamless experience for converting spoken content into written text.

## 🚀 Features

- **AI-Powered Transcription**: Uses Facebook's Wav2Vec 2.0 Large model for accurate speech recognition
- **Multiple Audio Formats**: Support for MP3, WAV, M4A, FLAC, and OGG audio files
- **User Authentication**: Secure login and registration system
- **Dashboard**: Personalized user dashboard with transcription history and statistics
- **File Management**: Upload, view, and manage audio transcriptions
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Copy & Download**: Easily copy or download transcription results

## 📋 Technical Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python, Flask
- **Database**: SQLAlchemy
- **Authentication**: Flask-Login
- **AI Model**: Wav2Vec 2.0 
- **Styling**: Font Awesome icons, Animate.css animations

## 🛠️ Project Structure

```
speech_recognition/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   ├── index.html
│   │   │   ├── history.html
│   │   │   └── view_recording.html
│   │   ├── transcribe/
│   │   │   ├── index.html
│   │   │   └── result.html
│   │   ├── partials/
│   │   │   └── navbar.html
│   │   ├── about.html
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   ├── models.py
│   └── routes/
└── requirements.txt
```

## 📌 Key Pages

- **Home Page**: Introduction to SpeechAI with feature highlights
- **Dashboard**: User dashboard showing statistics and recent transcriptions
- **Transcribe**: Upload audio files for transcription
- **History**: View and manage all past transcriptions
- **Profile**: User account management
- **About**: Information about the application and technology

## 🔧 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/speech_recognition.git
   cd speech_recognition
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Windows
   set FLASK_APP=app
   set FLASK_ENV=development
   
   # macOS/Linux
   export FLASK_APP=app
   export FLASK_ENV=development
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

7. Open your browser and navigate to `http://127.0.0.1:5000`

## 📱 Usage Guide

1. **Create an Account**: Register with a username, email, and password
2. **Login**: Access your personalized dashboard
3. **Upload Audio**: Navigate to the transcribe page and upload an audio file
4. **View Results**: See the transcription result and copy or download the text
5. **Manage History**: Access all your past transcriptions from the history page

## 💡 Tips for Best Results

- **Audio Quality**: Higher quality audio files result in more accurate transcriptions
- **Clear Speech**: Speak clearly and at a moderate pace
- **File Size**: Files under 10MB work best. For longer recordings, consider splitting into smaller segments
- **Processing Time**: Transcription typically takes 10-60 seconds depending on the length of your audio file

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/df1ea9a8-c7db-4a5c-9cc7-8f09f044faaf)
![image](https://github.com/user-attachments/assets/15bc2fe7-890c-41c2-a91e-39f556828163)
![image](https://github.com/user-attachments/assets/b06bd5b2-528a-4ba3-9a45-b850bb820f64)
![image](https://github.com/user-attachments/assets/0edc3e6a-a0b7-4222-bb6d-3b5f7e03b05e)
![image](https://github.com/user-attachments/assets/79b1fdd9-9854-4c2f-8f45-51557cadc1ee)


## 🔒 Security Features

- Secure user authentication
- Password hashing
- CSRF protection
- Private transcription storage
- Session management

## 🌟 Future Enhancements

- Real-time transcription
- Speaker diarization (multi-speaker detection)
- Additional language support
- Advanced editing tools
- Team collaboration features
- API access

## 📄 License

[Your License Information]

## 📞 Contact

For questions, suggestions, or support:
- Email: support@voicescribe.com
- [Your Contact Information]

---

Built with ❤️ using Flask and Wav2Vec 2.0 AI Technology
