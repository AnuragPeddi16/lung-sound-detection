from flask import Flask, render_template, request, jsonify, url_for
import os
from werkzeug.utils import secure_filename
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath('../CNN_Model'))

from CNN_predict import predict_class_cnn 

# Add the parent directory to sys.path
sys.path.append(os.path.abspath('../SVM_Model'))

from svm_predict import predict_class_svm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'wav'}

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_audio(filepath, method):

    if (method == True):
        result = predict_class_cnn(filepath)
        print("using cnn")
    else:
        result = predict_class_svm(filepath)
        print("using svm")
    
    return {
        'primary_condition': str(result[0]),  # Ensure it's a string
        'confidence': float(result[1]),       # Convert to float for JSON serialization
    }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    use_cnn = request.form['use_cnn']
    use_cnn = use_cnn == 'true'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the audio file
        results = analyze_audio(filepath, use_cnn)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify(results)
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)