### IMPORTS ###

from flask import Flask, request, jsonify, send_file, send_from_directory
from waitress import serve

import requests
import random
import logging
import os

### SETUP ###

app = Flask(__name__)

def clear_log(filename):
  with open(filename, 'w') as file:
    pass
    file.write('--- SERVER LOG ---\n\n')

def generate_signature():
  signature = ''
  for _ in range(20):
    signature += str(random.randint(0, 9))
  return signature

### SERVICES ###

# Delete Media Service:
@app.route('/delete_media', methods=['POST'])
def delete_media():
  data = request.get_json()
  filename = data['file'] + '.mp4'
  if os.path.exists('Media/' + filename):
    os.remove('Media/' + filename)
    return filename
  else:
    return filename, 404

# Request New Media Service:
@app.route('/new_media', methods=['POST'])
def get_new_media():
  files = os.listdir('Media')
  data = request.get_json()
  url = data['url']
  filename = data['file']

  if filename in files:
    filename += '_' + generate_signature() + '.mp4'
  else:
    filename += '.mp4'

  with requests.get(url, stream=True) as response:
    with open('Media/' + filename, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:
          file.write(chunk)
  return filename

# Media Files List Service:
@app.route('/media')
def get_media():
  files = os.listdir('Media')
  return jsonify(files)

# Media File Service:
@app.route('/media/<path:filename>')
def get_file(filename):
  return send_from_directory('Media', filename)

# Main Page Service:
@app.route('/')
def index():
  return send_file('index.html')

# Runs Server:
if __name__ == '__main__':
  filename = 'Media/server.log'
  clear_log(filename)
  logging.basicConfig(
    filename=filename,
    level=logging.DEBUG,
    format = '%(asctime)s %(message)s'
  )
  serve(app, host="0.0.0.0", port=1008)