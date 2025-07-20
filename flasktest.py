from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from datetime import datetime
from jinja2 import Environment, select_autoescape, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Sample data for demonstration
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "admin", "created_at": "2024-01-15"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "user", "created_at": "2024-01-16"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "role": "user", "created_at": "2024-01-17"}
]

# Enhanced HTML template with better styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flask Sample App</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f5f5f5;
        }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .nav-links { display: flex; justify-content: center; gap: 20px; margin: 20px 0; }
        .nav-links a { 
            text-decoration: none; 
            padding: 10px 20px; 
            background: #007bff; 
            color: white; 
            border-radius: 5px; 
            transition: background 0.3s;
        }
        .nav-links a:hover { background: #0056b3; }
        .user-card { 
            border: 1px solid #ddd; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px; 
            background: #f9f9f9;
        }
        .search-box { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .form-group { margin: 15px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select { 
            width: 100%; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .btn { 
            background: #28a745; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block;
        }
        .btn:hover { background: #218838; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .alert { 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 5px; 
            border: 1px solid transparent;
        }
        .alert-success { background: #d4edda; border-color: #c3e6cb; color: #155724; }
        .alert-error { background: #f8d7da; border-color: #f5c6cb; color: #721c24; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-card { 
            text-align: center; 
            padding: 20px; 
            background: #e9ecef; 
            border-radius: 8px; 
            flex: 1; 
            margin: 0 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Flask Sample Application</h1>
            <p>A comprehensive Flask application demonstrating various features</p>
        </div>
        
        <div class="nav-links">
            <a href="/">🏠 Home</a>
            <a href="/users">👥 Users</a>
            <a href="/api/users">🔌 API</a>
            <a href="/add-user">➕ Add User</a>
            <a href="/about">ℹ️ About</a>
            <a href="/stats">📊 Stats</a>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="content">
            <h2>Welcome to Flask Sample App</h2>
            <p>This application demonstrates various Flask features including:</p>
            <ul>
                <li>✅ Basic routing and URL handling</li>
                <li>✅ HTML responses with embedded styling</li>
                <li>✅ JSON API endpoints</li>
                <li>✅ Form handling and validation</li>
                <li>✅ URL parameters and dynamic routes</li>
                <li>✅ Flash messages for user feedback</li>
                <li>✅ Search functionality</li>
                <li>✅ Error handling</li>
            </ul>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>{{ users|length }}</h3>
                    <p>Total Users</p>
                </div>
                <div class="stat-card">
                    <h3>{{ users|selectattr('role', 'equalto', 'admin')|list|length }}</h3>
                    <p>Admin Users</p>
                </div>
                <div class="stat-card">
                    <h3>{{ users|selectattr('role', 'equalto', 'user')|list|length }}</h3>
                    <p>Regular Users</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Home page route with enhanced template"""
    return render_template_string(HTML_TEMPLATE, users=users)

@app.route('/users')
def get_users():
    """Display all users with search functionality"""
    search = request.args.get('search', '').lower()
    
    if search:
        filtered_users = [
            user for user in users 
            if search in user['name'].lower() or search in user['email'].lower()
        ]
    else:
        filtered_users = users
    
    user_list = ""
    for user in filtered_users:
        role_badge = f"<span style='background: {'#dc3545' if user['role'] == 'admin' else '#28a745'}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px;'>{user['role']}</span>"
        user_list += f"""
        <div class="user-card">
            <h3>ID: {user['id']} - {user['name']}</h3>
            <p><strong>Email:</strong> {user['email']}</p>
            <p><strong>Role:</strong> {role_badge}</p>
            <p><strong>Created:</strong> {user['created_at']}</p>
            <a href="/api/users/{user['id']}" class="btn">View JSON</a>
            <a href="/delete-user/{user['id']}" class="btn btn-danger" onclick="return confirm('Are you sure?')">Delete</a>
        </div>
        """
    
    search_form = f'''
    <form method="GET" action="/users">
        <input type="text" name="search" placeholder="Search users..." value="{search}" class="search-box">
        <button type="submit" class="btn">Search</button>
        <a href="/users" class="btn">Clear</a>
    </form>
    '''
    
    return f'''
    <div class="container">
        <div class="header">
            <h1>👥 Users Management</h1>
        </div>
        {search_form}
        <div class="content">
            <h2>Users List ({len(filtered_users)} found)</h2>
            {user_list if filtered_users else '<p>No users found matching your search.</p>'}
            <p><a href="/" class="btn">← Back to Home</a></p>
        </div>
    </div>
    '''

@app.route('/api/users')
def api_users():
    """API endpoint to get users as JSON"""
    return jsonify({
        "users": users,
        "total": len(users),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/users/<int:user_id>')
def api_user(user_id):
    """API endpoint to get a specific user by ID"""
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    """Add a new user with enhanced form"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'user')
        
        if not name or not email:
            flash('Name and email are required!', 'error')
            return redirect(url_for('add_user'))
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            flash('Email already exists!', 'error')
            return redirect(url_for('add_user'))
        
        new_id = max(user['id'] for user in users) + 1
        new_user = {
            "id": new_id, 
            "name": name, 
            "email": email, 
            "role": role,
            "created_at": datetime.now().strftime('%Y-%m-%d')
        }
        users.append(new_user)
        flash(f'User {name} added successfully!', 'success')
        return redirect(url_for('get_users'))
    
    return '''
    <div class="container">
        <div class="header">
            <h1>➕ Add New User</h1>
        </div>
        <div class="content">
            <form method="POST">
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="role">Role:</label>
                    <select id="role" name="role">
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <button type="submit" class="btn">Add User</button>
                <a href="/" class="btn">Cancel</a>
            </form>
        </div>
    </div>
    '''

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    """Delete a user"""
    global users
    original_length = len(users)
    users = [user for user in users if user['id'] != user_id]
    
    if len(users) < original_length:
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')
    
    return redirect(url_for('get_users'))

@app.route('/about')
def about():
    """About page with enhanced content"""
    return '''
    <div class="container">
        <div class="header">
            <h1>ℹ️ About This Flask App</h1>
        </div>
        <div class="content">
            <h2>Features Demonstrated</h2>
            <ul>
                <li><strong>Basic Routing:</strong> Multiple endpoints with different HTTP methods</li>
                <li><strong>HTML Responses:</strong> Dynamic HTML generation with embedded CSS</li>
                <li><strong>JSON API Endpoints:</strong> RESTful API for programmatic access</li>
                <li><strong>Form Handling:</strong> POST requests with data validation</li>
                <li><strong>URL Parameters:</strong> Dynamic routes with parameter extraction</li>
                <li><strong>Flash Messages:</strong> User feedback for actions</li>
                <li><strong>Search Functionality:</strong> Filter users by name or email</li>
                <li><strong>Error Handling:</strong> Proper HTTP status codes and error messages</li>
                <li><strong>Data Management:</strong> In-memory CRUD operations</li>
            </ul>
            
            <h2>API Endpoints</h2>
            <ul>
                <li><code>GET /api/users</code> - Get all users</li>
                <li><code>GET /api/users/{id}</code> - Get specific user</li>
                <li><code>GET /health</code> - Health check</li>
            </ul>
            
            <p><a href="/" class="btn">← Back to Home</a></p>
        </div>
    </div>
    '''

@app.route('/stats')
def stats():
    """Statistics page"""
    admin_count = len([u for u in users if u['role'] == 'admin'])
    user_count = len([u for u in users if u['role'] == 'user'])
    
    return f'''
    <div class="container">
        <div class="header">
            <h1>📊 Application Statistics</h1>
        </div>
        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <h3>{len(users)}</h3>
                    <p>Total Users</p>
                </div>
                <div class="stat-card">
                    <h3>{admin_count}</h3>
                    <p>Admin Users</p>
                </div>
                <div class="stat-card">
                    <h3>{user_count}</h3>
                    <p>Regular Users</p>
                </div>
            </div>
            
            <h2>User Distribution</h2>
            <p>Admins: {admin_count} ({admin_count/len(users)*100:.1f}%)</p>
            <p>Regular Users: {user_count} ({user_count/len(users)*100:.1f}%)</p>
            
            <p><a href="/" class="btn">← Back to Home</a></p>
        </div>
    </div>
    '''

@app.route('/health')
def health_check():
    """Health check endpoint with enhanced information"""
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users),
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler"""
    return '''
    <div class="container">
        <div class="header">
            <h1>❌ 404 - Page Not Found</h1>
        </div>
        <div class="content">
            <p>The page you're looking for doesn't exist.</p>
            <p><a href="/" class="btn">← Back to Home</a></p>
        </div>
    </div>
    ''', 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error handler"""
    return '''
    <div class="container">
        <div class="header">
            <h1>💥 500 - Internal Server Error</h1>
        </div>
        <div class="content">
            <p>Something went wrong on our end. Please try again later.</p>
            <p><a href="/" class="btn">← Back to Home</a></p>
        </div>
    </div>
    ''', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
