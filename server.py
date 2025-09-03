import os
from flask import Flask, request, jsonify
#from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
#from flask_cors import CORS

#UPLOAD_FOLDER = './uploads'
UPLOAD_FOLDER = '/tmp/uploads'

# In a serverless environment like Vercel, the directory needs to be writable.
# /tmp is the only writable directory.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#app = Flask(__name__, static_url_path='', static_folder='.')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#CORS(app)  # This will enable CORS for all routes
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#@app.route('/')
#def index():
#    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected file"}), 400

    uploaded_filenames = []
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_filenames.append(filename)
            
    print(f"Successfully uploaded {len(uploaded_filenames)} files.")
    return jsonify({"message": "Files uploaded successfully", "filenames": uploaded_filenames}), 200

#if __name__ == '__main__':
#    app.run(debug=True)
