from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)

# Sample data for demonstration
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
]

@app.route('/')
def home():
    """Home page route"""
    return '''
    <h1>Welcome to Flask Sample App</h1>
    <p>This is a sample Flask application with various routes:</p>
    <ul>
        <li><a href="/users">View Users</a></li>
        <li><a href="/api/users">API - Get Users</a></li>
        <li><a href="/add-user">Add New User</a></li>
        <li><a href="/about">About</a></li>
    </ul>
    '''

@app.route('/users')
def get_users():
    """Display all users"""
    user_list = ""
    for user in users:
        user_list += f"<li>ID: {user['id']} - {user['name']} ({user['email']})</li>"
    
    return f'''
    <h1>Users List</h1>
    <ul>{user_list}</ul>
    <p><a href="/">Back to Home</a></p>
    '''

@app.route('/api/users')
def api_users():
    """API endpoint to get users as JSON"""
    return jsonify(users)

@app.route('/api/users/<int:user_id>')
def api_user(user_id):
    """API endpoint to get a specific user by ID"""
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        if name and email:
            new_id = max(user['id'] for user in users) + 1
            new_user = {"id": new_id, "name": name, "email": email}
            users.append(new_user)
            return redirect(url_for('get_users'))
        else:
            return "Name and email are required!", 400
    
    return '''
    <h1>Add New User</h1>
    <form method="POST">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>
        <input type="submit" value="Add User">
    </form>
    <p><a href="/">Back to Home</a></p>
    '''

@app.route('/about')
def about():
    """About page"""
    return '''
    <h1>About This Flask App</h1>
    <p>This is a sample Flask application demonstrating:</p>
    <ul>
        <li>Basic routing</li>
        <li>HTML responses</li>
        <li>JSON API endpoints</li>
        <li>Form handling</li>
        <li>URL parameters</li>
        <li>Redirects</li>
    </ul>
    <p><a href="/">Back to Home</a></p>
    '''

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Flask app is running"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
