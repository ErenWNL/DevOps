from flask import Flask, request, jsonify, render_template_string, redirect, flash, session
from datetime import datetime
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'blog-secret-key-here'

# In-memory storage
posts = []
users = [
    {
        "id": "1",
        "username": "admin",
        "email": "admin@blog.com",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "created_at": "2024-01-01"
    },
    {
        "id": "2", 
        "username": "john_doe",
        "email": "john@example.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "role": "author",
        "created_at": "2024-01-15"
    }
]

# Sample posts
sample_posts = [
    {
        "id": "1",
        "title": "Getting Started with Flask",
        "content": "Flask is a lightweight web framework for Python that makes it easy to build web applications. In this post, we'll explore the basics of Flask and how to create your first application.",
        "author_id": "1",
        "author_name": "admin",
        "tags": ["python", "flask", "web-development"],
        "status": "published",
        "created_at": "2024-01-15 10:00:00",
        "updated_at": "2024-01-15 10:00:00",
        "views": 150,
        "likes": 25,
        "comments": []
    },
    {
        "id": "2",
        "title": "Building REST APIs with Flask",
        "content": "REST APIs are essential for modern web applications. Learn how to build robust APIs using Flask-RESTful and best practices for API design.",
        "author_id": "2",
        "author_name": "john_doe", 
        "tags": ["api", "rest", "flask", "python"],
        "status": "published",
        "created_at": "2024-01-16 14:30:00",
        "updated_at": "2024-01-16 14:30:00",
        "views": 89,
        "likes": 12,
        "comments": []
    }
]

posts.extend(sample_posts)

# HTML template for the blog
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flask Blog</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f8f9fa;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px 0;
            margin-bottom: 30px;
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-links { display: flex; gap: 20px; }
        .nav-links a { 
            color: white; 
            text-decoration: none; 
            padding: 8px 16px;
            border-radius: 20px;
            transition: background 0.3s;
        }
        .nav-links a:hover { background: rgba(255,255,255,0.2); }
        .main-content { display: flex; gap: 30px; }
        .posts-section { flex: 2; }
        .sidebar { flex: 1; }
        .post-card { 
            background: white; 
            border-radius: 10px; 
            padding: 25px; 
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .post-card:hover { transform: translateY(-2px); }
        .post-title { 
            font-size: 1.5em; 
            color: #333; 
            margin-bottom: 10px;
            text-decoration: none;
        }
        .post-title:hover { color: #667eea; }
        .post-meta { 
            color: #666; 
            font-size: 14px; 
            margin-bottom: 15px;
        }
        .post-excerpt { 
            color: #555; 
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .post-tags { 
            display: flex; 
            gap: 8px; 
            margin-bottom: 15px;
        }
        .tag { 
            background: #e9ecef; 
            color: #495057; 
            padding: 4px 12px; 
            border-radius: 15px; 
            font-size: 12px;
        }
        .post-stats { 
            display: flex; 
            gap: 20px; 
            color: #666; 
            font-size: 14px;
        }
        .sidebar-card { 
            background: white; 
            border-radius: 10px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block;
        }
        .btn:hover { opacity: 0.9; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input, .form-group textarea { 
            width: 100%; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .alert { 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 5px; 
            border: 1px solid transparent;
        }
        .alert-success { background: #d4edda; border-color: #c3e6cb; color: #155724; }
        .alert-error { background: #f8d7da; border-color: #f5c6cb; color: #721c24; }
        .user-info { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 15px;
        }
        .comment { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 10px 0;
        }
        .comment-meta { 
            font-size: 12px; 
            color: #666; 
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📝 Flask Blog</h1>
            <nav class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/posts">📄 Posts</a>
                {% if session.get('user_id') %}
                    <a href="/new-post">✏️ New Post</a>
                    <a href="/profile">👤 Profile</a>
                    <a href="/logout">🚪 Logout</a>
                {% else %}
                    <a href="/login">🔑 Login</a>
                    <a href="/register">📝 Register</a>
                {% endif %}
            </nav>
        </div>
    </div>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="main-content">
            <div class="posts-section">
                {% if posts %}
                    {% for post in posts %}
                    <article class="post-card">
                        <h2><a href="/post/{{ post.id }}" class="post-title">{{ post.title }}</a></h2>
                        <div class="post-meta">
                            By {{ post.author_name }} • {{ post.created_at }} • {{ post.views }} views
                        </div>
                        <div class="post-excerpt">
                            {{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}
                        </div>
                        <div class="post-tags">
                            {% for tag in post.tags %}
                            <span class="tag">#{{ tag }}</span>
                            {% endfor %}
                        </div>
                        <div class="post-stats">
                            <span>❤️ {{ post.likes }} likes</span>
                            <span>💬 {{ post.comments|length }} comments</span>
                        </div>
                    </article>
                    {% endfor %}
                {% else %}
                    <div class="post-card">
                        <h2>No posts yet</h2>
                        <p>Be the first to create a post!</p>
                        {% if session.get('user_id') %}
                            <a href="/new-post" class="btn">Create Post</a>
                        {% else %}
                            <a href="/login" class="btn">Login to Create Post</a>
                        {% endif %}
                    </div>
                {% endif %}
            </div>

            <div class="sidebar">
                <div class="sidebar-card">
                    <h3>👤 User Info</h3>
                    {% if session.get('user_id') %}
                        <div class="user-info">
                            <p><strong>Welcome, {{ session.get('username') }}!</strong></p>
                            <p>Role: {{ session.get('role') }}</p>
                        </div>
                    {% else %}
                        <p>Please <a href="/login">login</a> to create posts and comment.</p>
                    {% endif %}
                </div>

                <div class="sidebar-card">
                    <h3>📊 Blog Stats</h3>
                    <p>Total Posts: {{ posts|length }}</p>
                    <p>Total Users: {{ users|length }}</p>
                    <p>Total Comments: {{ posts|sum(attribute='comments|length') }}</p>
                </div>

                <div class="sidebar-card">
                    <h3>🏷️ Popular Tags</h3>
                    {% set all_tags = [] %}
                    {% for post in posts %}
                        {% for tag in post.tags %}
                            {% if tag not in all_tags %}
                                {% set _ = all_tags.append(tag) %}
                            {% endif %}
                        {% endfor %}
                    {% endfor %}
                    {% for tag in all_tags[:10] %}
                        <span class="tag">{{ tag }}</span>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Home page showing all posts"""
    return render_template_string(HTML_TEMPLATE, posts=posts, users=users)

@app.route('/post/<post_id>')
def view_post(post_id):
    """View a specific post with comments"""
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        flash('Post not found!', 'error')
        return redirect('/')
    
    # Increment view count
    post['views'] += 1
    
    return f'''
    <div class="header">
        <div class="header-content">
            <h1>📝 Flask Blog</h1>
            <nav class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/posts">📄 Posts</a>
                <a href="/post/{post_id}">📄 Current Post</a>
            </nav>
        </div>
    </div>

    <div class="container">
        <div class="main-content">
            <div class="posts-section">
                <article class="post-card">
                    <h1 class="post-title">{post['title']}</h1>
                    <div class="post-meta">
                        By {post['author_name']} • {post['created_at']} • {post['views']} views
                    </div>
                    <div class="post-tags">
                        {% for tag in post['tags'] %}
                        <span class="tag">#{tag}</span>
                        {% endfor %}
                    </div>
                    <div class="post-excerpt" style="font-size: 16px; line-height: 1.8;">
                        {post['content']}
                    </div>
                    <div class="post-stats">
                        <span>❤️ {post['likes']} likes</span>
                        <span>💬 {len(post['comments'])} comments</span>
                    </div>
                </article>

                <div class="post-card">
                    <h3>💬 Comments ({len(post['comments'])})</h3>
                    {% if post['comments'] %}
                        {% for comment in post['comments'] %}
                        <div class="comment">
                            <div class="comment-meta">
                                By {comment['author']} • {comment['created_at']}
                            </div>
                            <div>{comment['content']}</div>
                        </div>
                        {% endfor %}
                    {% else %}
                        <p>No comments yet. Be the first to comment!</p>
                    {% endif %}

                    {% if session.get('user_id') %}
                    <form method="POST" action="/post/{post_id}/comment" style="margin-top: 20px;">
                        <div class="form-group">
                            <label for="comment">Add a comment:</label>
                            <textarea name="comment" rows="3" required></textarea>
                        </div>
                        <button type="submit" class="btn">Post Comment</button>
                    </form>
                    {% else %}
                    <p><a href="/login">Login</a> to add a comment.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    '''

@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    """Add a comment to a post"""
    if not session.get('user_id'):
        flash('Please login to comment!', 'error')
        return redirect(f'/post/{post_id}')
    
    comment_content = request.form.get('comment', '').strip()
    if not comment_content:
        flash('Comment cannot be empty!', 'error')
        return redirect(f'/post/{post_id}')
    
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        flash('Post not found!', 'error')
        return redirect('/')
    
    comment = {
        'id': str(uuid.uuid4()),
        'content': comment_content,
        'author': session.get('username'),
        'author_id': session.get('user_id'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    post['comments'].append(comment)
    flash('Comment added successfully!', 'success')
    return redirect(f'/post/{post_id}')

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    """Create a new post"""
    if not session.get('user_id'):
        flash('Please login to create posts!', 'error')
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect('/new-post')
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        post = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': content,
            'author_id': session.get('user_id'),
            'author_name': session.get('username'),
            'tags': tag_list,
            'status': 'published',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'views': 0,
            'likes': 0,
            'comments': []
        }
        
        posts.append(post)
        flash('Post created successfully!', 'success')
        return redirect(f'/post/{post["id"]}')
    
    return '''
    <div class="header">
        <div class="header-content">
            <h1>📝 Flask Blog</h1>
            <nav class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/posts">📄 Posts</a>
                <a href="/new-post">✏️ New Post</a>
            </nav>
        </div>
    </div>

    <div class="container">
        <div class="main-content">
            <div class="posts-section">
                <div class="post-card">
                    <h2>✏️ Create New Post</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label for="title">Title:</label>
                            <input type="text" id="title" name="title" required>
                        </div>
                        <div class="form-group">
                            <label for="content">Content:</label>
                            <textarea id="content" name="content" rows="10" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="tags">Tags (comma-separated):</label>
                            <input type="text" id="tags" name="tags" placeholder="python, flask, web-development">
                        </div>
                        <button type="submit" class="btn">Create Post</button>
                        <a href="/" class="btn">Cancel</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect('/login')
        
        user = next((u for u in users if u['username'] == username), None)
        if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {username}!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password!', 'error')
            return redirect('/login')
    
    return '''
    <div class="header">
        <div class="header-content">
            <h1>📝 Flask Blog</h1>
            <nav class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/login">🔑 Login</a>
            </nav>
        </div>
    </div>

    <div class="container">
        <div class="main-content">
            <div class="posts-section">
                <div class="post-card">
                    <h2>🔑 Login</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn">Login</button>
                        <a href="/register" class="btn">Register</a>
                    </form>
                    <p style="margin-top: 15px;">
                        <strong>Demo accounts:</strong><br>
                        Username: admin, Password: admin123<br>
                        Username: john_doe, Password: password123
                    </p>
                </div>
            </div>
        </div>
    </div>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return redirect('/register')
        
        # Check if username already exists
        if any(u['username'] == username for u in users):
            flash('Username already exists!', 'error')
            return redirect('/register')
        
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'password_hash': hashlib.sha256(password.encode()).hexdigest(),
            'role': 'user',
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        
        users.append(new_user)
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    
    return '''
    <div class="header">
        <div class="header-content">
            <h1>📝 Flask Blog</h1>
            <nav class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/register">📝 Register</a>
            </nav>
        </div>
    </div>

    <div class="container">
        <div class="main-content">
            <div class="posts-section">
                <div class="post-card">
                    <h2>📝 Register</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email:</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn">Register</button>
                        <a href="/login" class="btn">Login</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
    '''

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/')

@app.route('/api/posts')
def api_posts():
    """API endpoint to get all posts"""
    return jsonify({
        "posts": posts,
        "total": len(posts),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/posts/<post_id>')
def api_post(post_id):
    """API endpoint to get a specific post"""
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route('/api/users')
def api_users():
    """API endpoint to get all users (without passwords)"""
    safe_users = []
    for user in users:
        safe_user = user.copy()
        safe_user.pop('password_hash', None)
        safe_users.append(safe_user)
    return jsonify(safe_users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 