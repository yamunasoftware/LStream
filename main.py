from flask import Flask, jsonify, send_file, send_from_directory
from waitress import serve
import os

app = Flask(__name__)

@app.route('/media')
def get_media():
  files = os.listdir('Media')
  return jsonify(files)

@app.route('/media/<path:filename>')
def get_file(filename):
  return send_from_directory('Media', filename)

@app.route('/')
def index():
  return send_file('index.html')

if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=1008)