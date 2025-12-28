### IMPORTS ###

from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
import requests
import subprocess
import os

### SETUP ###

# Initialize Flask App:
os.environ['BUSY'] = 'FALSE'
app = Flask(__name__)

# Converts Video to Standard Playback Format:
def convert_video(filename):
  input_file = 'media/' + filename
  output_file = 'media/staged_' + filename

  cmd = [
    'ffmpeg',
    '-i', input_file,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-strict', 'experimental',
    '-loglevel', 'error',
    output_file
  ]
  code = subprocess.run(cmd, check=True).returncode

  if code != 0:
    raise RuntimeError('FFMPEG Conversion Failed')

  os.remove(input_file)
  os.rename(output_file, input_file)

### ENDPOINTS ###

# Add Video Endpoint:
@app.route('/add_video', methods=['POST'])
def add_video():
  try:
    data = request.get_json()
    url = data['url']
    filename = data['name'].replace('.mp4', '') + '.mp4'

    if filename in os.listdir('media/'):
      return 'Invalid Name', 409

    if os.environ['BUSY'] == 'FALSE':
      os.environ['BUSY'] = 'TRUE'
      response = requests.get(url, stream=True)
      with open('media/' + filename, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10*1024):
          file.write(chunk)

      convert_video(filename)
      os.environ['BUSY'] = 'FALSE'
      return 'Success', 200
    
    else:
      return 'Server Busy', 503
    
  except:
    os.remove('media/' + filename)
    os.environ['BUSY'] = 'FALSE'
    return 'Server Error', 500

# Get Videos Endpoint:
@app.route('/get_videos')
def get_videos():
  try:
    if os.environ['BUSY'] == 'FALSE':
      files = []
      for file in os.listdir('media/'):
        if file.endswith('.mp4'):
          files.append(file.replace('.mp4', ''))
      return jsonify(files), 200
    
    else:
      return 'Server Busy', 503
    
  except:
    return 'Server Error', 500

# Video File Endpoint:
@app.route('/<path:filename>')
def get_file(filename):
  try:
    if os.environ['BUSY'] == 'FALSE':
      file = filename.replace('.mp4', '') + '.mp4'
      return send_from_directory('/main/media', file, mimetype='video/mp4', as_attachment=False)
    else:
      return 'Server Busy', 503

  except:
    return 'Server Error', 500

# Main Page Endpoint:
@app.route('/')
def index():
  try:
    return render_template('index.html'), 200
    
  except:
    return 'Server Error', 500
  
# Runs Server:
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=1008, debug=True)