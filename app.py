import os
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/gallery')
def gallery():
    json_path = os.path.join(app.root_path, 'JSON', 'gallery.json')
    with open(json_path, 'r') as f:
        gallery_data = json.load(f)
    
    # Sort data: latest date first (Descending order)
    # Assuming Date format is YYYY-MM-DD
    sorted_gallery = sorted(gallery_data, key=lambda x: x['Date'], reverse=True)
    
    return render_template('gallery.html', gallery=sorted_gallery)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/coffee')
def coffee():
    return "Comming soon"

if __name__ == '__main__':
    app.run(debug=True)