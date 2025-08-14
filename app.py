from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
import os
import uuid
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configuration
DATA_DIR = os.environ.get('DATA_DIR', 'data')
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
CONVERTED_FOLDER = os.path.join(DATA_DIR, 'converted')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)
os.makedirs('static/examples', exist_ok=True)

# Hardcoded credentials (change in production)
USERS = {
    'admin': generate_password_hash('password123')
}

# Mock conversion history storage
conversion_history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                flash('File size is too large (max 10MB)', 'error')
                return redirect(request.url)
            
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            session['uploaded_file'] = unique_filename
            session['original_filename'] = filename
            return redirect(url_for('configure'))
        else:
            flash('Invalid file type. Please use JPG, PNG, or PDF files.', 'error')
    
    return render_template('upload.html')

@app.route('/configure')
@login_required
def configure():
    if 'uploaded_file' not in session:
        return redirect(url_for('upload'))
    return render_template('configure.html')

@app.route('/process', methods=['POST'])
@login_required
def process():
    if 'uploaded_file' not in session:
        return redirect(url_for('upload'))
    
    # Get configuration from form
    config = {
        'output_format': request.form.get('output_format', 'dwg'),
        'quality': request.form.get('quality', 'balanced'),
        'scale': request.form.get('scale', 'auto'),
        'line_detection': request.form.get('line_detection', 'normal'),
        'text_recognition': request.form.get('text_recognition', 'on'),
        'color_handling': request.form.get('color_handling', 'preserve')
    }
    
    session['config'] = config
    return render_template('processing.html')

@app.route('/api/convert')
@login_required
def convert_api():
    if 'uploaded_file' not in session:
        return jsonify({'error': 'No file uploaded'}), 400
    
    # Mock conversion process with stages
    stages = [
        {'name': 'Analyzing image content...', 'duration': 2},
        {'name': 'Detecting lines and shapes...', 'duration': 3},
        {'name': 'Converting to vector format...', 'duration': 4},
        {'name': 'Optimizing CAD file...', 'duration': 2},
        {'name': 'Preparing download...', 'duration': 1}
    ]
    
    # Simulate processing time
    time.sleep(1)
    
    # Create mock converted file
    converted_filename = f"converted_{uuid.uuid4()}.dwg"
    converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)
    
    # Create a dummy file (in real implementation, this would be the actual conversion)
    with open(converted_path, 'w') as f:
        f.write("Mock CAD file content")
    
    # Add to conversion history
    conversion_record = {
        'id': str(uuid.uuid4()),
        'original_filename': session.get('original_filename', 'unknown'),
        'converted_filename': converted_filename,
        'timestamp': datetime.now().isoformat(),
        'processing_time': 12,  # seconds
        'elements_detected': 47,
        'file_size': '2.1 MB',
        'quality': session.get('config', {}).get('quality', 'balanced'),
        'config': session.get('config', {})
    }
    
    conversion_history.append(conversion_record)
    session['conversion_result'] = conversion_record
    
    return jsonify({'status': 'complete', 'redirect': url_for('results')})

@app.route('/results')
@login_required
def results():
    if 'conversion_result' not in session:
        return redirect(url_for('index'))
    
    result = session['conversion_result']
    recent_conversions = conversion_history[-5:]  # Last 5 conversions
    
    return render_template('results.html', result=result, recent_conversions=recent_conversions)

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    try:
        return send_file(os.path.join(CONVERTED_FOLDER, filename), as_attachment=True)
    except FileNotFoundError:
        flash('File not found', 'error')
        return redirect(url_for('results'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
