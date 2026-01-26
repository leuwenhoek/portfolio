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

@app.route('/contact')
def contact():
    # Linking to your Buy Me a Coffee as the contact point
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)