from flask import Flask, request, jsonify, render_template_string, redirect
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for todos (in a real app, you'd use a database)
todos = []

# HTML template for the todo app
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .todo-item { border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px; }
        .completed { background-color: #f0f0f0; text-decoration: line-through; }
        .form-group { margin: 10px 0; }
        input[type="text"], textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .delete-btn { background-color: #f44336; }
        .delete-btn:hover { background-color: #da190b; }
        .complete-btn { background-color: #2196F3; }
        .complete-btn:hover { background-color: #0b7dda; }
    </style>
</head>
<body>
    <h1>Todo Application</h1>
    
    <h2>Add New Todo</h2>
    <form method="POST" action="/add">
        <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" required>
        </div>
        <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" name="description" rows="3"></textarea>
        </div>
        <div class="form-group">
            <label for="priority">Priority:</label>
            <select id="priority" name="priority">
                <option value="low">Low</option>
                <option value="medium" selected>Medium</option>
                <option value="high">High</option>
            </select>
        </div>
        <button type="submit">Add Todo</button>
    </form>
    
    <h2>Your Todos</h2>
    {% if todos %}
        {% for todo in todos %}
        <div class="todo-item {% if todo.completed %}completed{% endif %}">
            <h3>{{ todo.title }}</h3>
            <p><strong>Description:</strong> {{ todo.description or 'No description' }}</p>
            <p><strong>Priority:</strong> <span style="color: {% if todo.priority == 'high' %}#f44336{% elif todo.priority == 'medium' %}#ff9800{% else %}#4CAF50{% endif %}">{{ todo.priority.title() }}</span></p>
            <p><strong>Created:</strong> {{ todo.created_at }}</p>
            {% if todo.completed %}
                <p><strong>Completed:</strong> {{ todo.completed_at }}</p>
            {% endif %}
            <div>
                {% if not todo.completed %}
                <a href="/complete/{{ todo.id }}"><button class="complete-btn">Mark Complete</button></a>
                {% endif %}
                <a href="/delete/{{ todo.id }}"><button class="delete-btn">Delete</button></a>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <p>No todos yet. Add one above!</p>
    {% endif %}
    
    <h2>API Endpoints</h2>
    <ul>
        <li><a href="/api/todos">GET /api/todos</a> - Get all todos as JSON</li>
        <li><a href="/api/todos/active">GET /api/todos/active</a> - Get active todos</li>
        <li><a href="/api/todos/completed">GET /api/todos/completed</a> - Get completed todos</li>
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    """Main todo app page"""
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    title = request.form.get('title')
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')
    
    if not title:
        return "Title is required!", 400
    
    todo = {
        'id': str(uuid.uuid4()),
        'title': title,
        'description': description,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'completed_at': None
    }
    
    todos.append(todo)
    return redirect('/')

@app.route('/complete/<todo_id>')
def complete_todo(todo_id):
    """Mark a todo as completed"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    return redirect('/')

@app.route('/delete/<todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect('/')

@app.route('/api/todos')
def api_todos():
    """API endpoint to get all todos"""
    return jsonify(todos)

@app.route('/api/todos/active')
def api_active_todos():
    """API endpoint to get active todos"""
    active_todos = [todo for todo in todos if not todo['completed']]
    return jsonify(active_todos)

@app.route('/api/todos/completed')
def api_completed_todos():
    """API endpoint to get completed todos"""
    completed_todos = [todo for todo in todos if todo['completed']]
    return jsonify(completed_todos)

@app.route('/api/todos/<todo_id>')
def api_todo(todo_id):
    """API endpoint to get a specific todo"""
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    """API endpoint to delete a todo"""
    global todos
    original_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    
    if len(todos) < original_length:
        return jsonify({"message": "Todo deleted successfully"})
    return jsonify({"error": "Todo not found"}), 404

@app.route('/api/todos/<todo_id>/complete', methods=['PUT'])
def api_complete_todo(todo_id):
    """API endpoint to mark a todo as completed"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 