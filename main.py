### IMPORTS ###

from flask import Flask, request, jsonify, send_file, send_from_directory
from waitress import serve

import requests
import random
import logging
import os

### SETUP ###

os.environ['MANAGE'] = 'FALSE'
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
  if os.environ['MANAGE'] == 'FALSE':
    try:
      os.environ['MANAGE'] = 'TRUE'
      data = request.get_json()
      filename = data['file'].replace('.', '').replace('/', '').replace('\\', '')
      filename += '.mp4'

      if os.path.exists('media/' + filename):
        os.remove('media/' + filename)
        os.environ['MANAGE'] = 'FALSE'
        return 'Success', 200
      
      else:
        os.environ['MANAGE'] = 'FALSE'
        return 'Not Found', 404
    
    except:
      os.environ['MANAGE'] = 'FALSE'
      return 'Server Error', 500
  
  else:
    return send_file('resources/busy.html'), 503

# Request New Media Service:
@app.route('/new_media', methods=['POST'])
def get_new_media():
  if os.environ['MANAGE'] == 'FALSE':
    try:
      os.environ['MANAGE'] = 'TRUE'
      files = os.listdir('media')

      data = request.get_json()
      url = data['url']
      filename = data['file']

      if filename in files:
        filename += '_' + generate_signature() + '.mp4'
      else:
        filename += '.mp4'

      with requests.get(url, stream=True) as response:
        with open('media/' + filename, 'wb') as file:
          for chunk in response.iter_content(chunk_size=8192):
            if chunk:
              file.write(chunk)
      
      os.environ['MANAGE'] = 'FALSE'
      return 'Success', 200
    
    except:
      os.environ['MANAGE'] = 'FALSE'
      return 'Server Error', 500
  
  else:
    return send_file('resources/busy.html'), 503

# Media Files List Service:
@app.route('/media')
def get_media():
  if os.environ['MANAGE'] == 'FALSE':
    files = os.listdir('media')
    return jsonify(files), 200
  
  else:
    return send_file('resources/busy.html'), 503

# Media File Service:
@app.route('/media/<path:filename>')
def get_file(filename):
  if os.environ['MANAGE'] == 'FALSE':
    return send_from_directory('media', filename), 200
  
  else:
    return send_file('resources/busy.html'), 503

# Main Page Service:
@app.route('/')
def index():
  if os.environ['MANAGE'] == 'FALSE':
    return send_file('resources/index.html'), 200
  
  else:
    return send_file('resources/busy.html'), 503
  
# Runs Server:
if __name__ == '__main__':
  filename = 'resources/server.log'
  clear_log(filename)
  logging.basicConfig(
    filename=filename,
    level=logging.DEBUG,
    format = '%(asctime)s %(message)s'
  )
  serve(app, host="0.0.0.0", port=1008)