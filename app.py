import os
import json
import time
import threading
import urllib.request
from datetime import datetime
from flask import Flask, render_template, redirect, make_response, send_from_directory, request

app = Flask(__name__)

@app.before_request
def enforce_canonical_domain():
    host = request.headers.get('Host', '')
    if host.startswith('www.') and 'localhost' not in host and '127.0.0.1' not in host:
        canonical_host = host[4:]
        url = f"https://{canonical_host}{request.path}"
        if request.query_string:
            url += f"?{request.query_string.decode('utf-8')}"
        return redirect(url, code=301)

def clear_leetcode_cache():
    try:
        req = urllib.request.Request("https://leetcard.jacoblin.cool/us/leuwenhoek", method="DELETE")
        with urllib.request.urlopen(req, timeout=5) as response:
            response.read()
    except Exception:
        pass

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/stats')
def stats():
    threading.Thread(target=clear_leetcode_cache).start()
    return render_template('stats.html', timestamp=int(time.time()))

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
    return redirect('https://buymeacoffee.com/leuwenhoek', code=301)

@app.context_processor
def inject_site_url():
    site_url = os.environ.get('SITE_URL', 'https://leuwenhoek.xyz').rstrip('/')
    return dict(site_url=site_url)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'favicons'), 'favicon.ico')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'favicons'), 'apple-touch-icon.png')

@app.route('/robots.txt')
def robots_txt():
    try:
        with open(os.path.join(app.root_path, 'robots.txt'), 'r', encoding='utf-8') as f:
            content = f.read().strip()
        response = make_response(content)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    except Exception:
        return send_from_directory(app.root_path, 'robots.txt')

@app.route('/robot.txt')
def robot_txt():
    return redirect('/robots.txt', code=301)

@app.route('/sitemap.xml')
def sitemap_xml():
    try:
        with open(os.path.join(app.root_path, 'sitemap.xml'), 'r', encoding='utf-8') as f:
            content = f.read().strip()
        response = make_response(content)
        response.headers['Content-Type'] = 'application/xml; charset=utf-8'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    except Exception:
        return send_from_directory(app.root_path, 'sitemap.xml')

if __name__ == '__main__':
    app.run(debug=True)