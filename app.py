from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes import api
app = Flask(__name__, static_folder='frontend')
CORS(app)
app.register_blueprint(api, url_prefix='/api')
@app.route('/')
def index(): return send_from_directory('frontend','index.html')
@app.route('/<path:path>')
def static_files(path): return send_from_directory('frontend',path)
if __name__ == '__main__': app.run(host='127.0.0.1',port=5000,debug=True)
