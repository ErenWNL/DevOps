from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    """Simple home page - serves the HTML file directly"""
    return send_file('index.html')

@app.route('/about')
def about():
    """Simple about page"""
    return '''
    <h1>About</h1>
    <p>This is a simple Flask application.</p>
    <a href="/">Back to Home</a>
    '''

@app.route('/contact')
def contact():
    """Simple contact page"""
    return '''
    <h1>Contact</h1>
    <p>Email: contact@example.com</p>
    <p>Phone: 123-456-7890</p>
    <a href="/">Back to Home</a>
    '''

@app.route('/hello/<name>')
def hello(name):
    """Simple greeting page"""
    return f'''
    <h1>Hello, {name}!</h1>
    <p>Welcome to our simple Flask app.</p>
    <a href="/">Back to Home</a>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000) 