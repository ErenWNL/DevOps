from flask import Flask, request, jsonify, render_template_string, redirect, flash
from datetime import datetime, timedelta
import uuid
import json

app = Flask(__name__)
app.secret_key = 'todo-secret-key-here'

# In-memory storage for todos (in a real app, you'd use a database)
todos = []

# Sample categories
categories = [
    {"id": "work", "name": "Work", "color": "#ff6b6b"},
    {"id": "personal", "name": "Personal", "color": "#4ecdc4"},
    {"id": "shopping", "name": "Shopping", "color": "#45b7d1"},
    {"id": "health", "name": "Health", "color": "#96ceb4"},
    {"id": "learning", "name": "Learning", "color": "#feca57"}
]

# Enhanced HTML template with better styling and features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Todo App</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px; 
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .content { padding: 30px; }
        .form-section { 
            background: #f8f9fa; 
            padding: 25px; 
            border-radius: 10px; 
            margin-bottom: 30px;
        }
        .form-row { display: flex; gap: 15px; margin-bottom: 15px; }
        .form-group { flex: 1; }
        .form-group label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #333;
        }
        .form-group input, .form-group select, .form-group textarea { 
            width: 100%; 
            padding: 12px; 
            border: 2px solid #e9ecef; 
            border-radius: 8px; 
            font-size: 14px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { 
            outline: none; 
            border-color: #667eea;
        }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-danger { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); }
        .btn-success { background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); }
        .btn-warning { background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }
        .todo-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 20px; 
            margin-top: 20px;
        }
        .todo-item { 
            border: 2px solid #e9ecef; 
            padding: 20px; 
            border-radius: 12px; 
            background: white;
            transition: all 0.3s;
            position: relative;
        }
        .todo-item:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .todo-item.completed { 
            background: #f8f9fa; 
            border-color: #28a745;
        }
        .todo-item.completed h3 { text-decoration: line-through; color: #6c757d; }
        .todo-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            margin-bottom: 15px;
        }
        .todo-title { 
            font-size: 1.2em; 
            font-weight: 600; 
            color: #333;
            margin-right: 10px;
        }
        .category-badge { 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: 600; 
            color: white;
            white-space: nowrap;
        }
        .priority-badge { 
            padding: 2px 8px; 
            border-radius: 12px; 
            font-size: 11px; 
            font-weight: 600; 
            color: white;
            margin-left: 8px;
        }
        .priority-high { background: #dc3545; }
        .priority-medium { background: #ffc107; color: #212529; }
        .priority-low { background: #28a745; }
        .todo-meta { 
            font-size: 12px; 
            color: #6c757d; 
            margin: 10px 0;
        }
        .todo-actions { 
            display: flex; 
            gap: 10px; 
            margin-top: 15px;
        }
        .todo-actions .btn { padding: 8px 15px; font-size: 12px; }
        .due-date { 
            font-weight: 600; 
            margin: 5px 0;
        }
        .due-date.overdue { color: #dc3545; }
        .due-date.today { color: #ffc107; }
        .due-date.future { color: #28a745; }
        .stats-section { 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px;
        }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 15px;
        }
        .stat-card { 
            text-align: center; 
            padding: 20px; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-number { 
            font-size: 2em; 
            font-weight: 700; 
            color: #667eea;
        }
        .filters { 
            display: flex; 
            gap: 15px; 
            margin-bottom: 20px; 
            flex-wrap: wrap;
        }
        .filter-btn { 
            padding: 8px 16px; 
            border: 2px solid #667eea; 
            background: white; 
            color: #667eea; 
            border-radius: 20px; 
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn.active { 
            background: #667eea; 
            color: white;
        }
        .empty-state { 
            text-align: center; 
            padding: 50px; 
            color: #6c757d;
        }
        .empty-state h3 { margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Advanced Todo App</h1>
            <p>Organize your tasks with categories, priorities, and due dates</p>
        </div>
        
        <div class="content">
            <div class="form-section">
                <h2>➕ Add New Todo</h2>
                <form method="POST" action="/add">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="title">Title *</label>
                            <input type="text" id="title" name="title" required placeholder="Enter todo title">
                        </div>
                        <div class="form-group">
                            <label for="category">Category</label>
                            <select id="category" name="category">
                                <option value="">Select category</option>
                                {% for cat in categories %}
                                <option value="{{ cat.id }}">{{ cat.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="priority">Priority</label>
                            <select id="priority" name="priority">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="due_date">Due Date</label>
                            <input type="datetime-local" id="due_date" name="due_date">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea id="description" name="description" rows="3" placeholder="Add details about this todo..."></textarea>
                    </div>
                    <button type="submit" class="btn">Add Todo</button>
                </form>
            </div>

            <div class="stats-section">
                <h2>📊 Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{{ todos|length }}</div>
                        <div>Total Todos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ todos|selectattr('completed', 'equalto', false)|list|length }}</div>
                        <div>Active</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ todos|selectattr('completed', 'equalto', true)|list|length }}</div>
                        <div>Completed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ todos|selectattr('priority', 'equalto', 'high')|list|length }}</div>
                        <div>High Priority</div>
                    </div>
                </div>
            </div>

            <div class="filters">
                <button class="filter-btn active" onclick="filterTodos('all')">All</button>
                <button class="filter-btn" onclick="filterTodos('active')">Active</button>
                <button class="filter-btn" onclick="filterTodos('completed')">Completed</button>
                <button class="filter-btn" onclick="filterTodos('high')">High Priority</button>
                <button class="filter-btn" onclick="filterTodos('overdue')">Overdue</button>
            </div>

            <div class="todo-grid" id="todoGrid">
                {% if todos %}
                    {% for todo in todos %}
                    <div class="todo-item {% if todo.completed %}completed{% endif %}" data-priority="{{ todo.priority }}" data-status="{% if todo.completed %}completed{% else %}active{% endif %}">
                        <div class="todo-header">
                            <div>
                                <h3 class="todo-title">{{ todo.title }}</h3>
                                {% if todo.category %}
                                <span class="category-badge" style="background-color: {{ categories|selectattr('id', 'equalto', todo.category)|first|attr('color') }}">{{ categories|selectattr('id', 'equalto', todo.category)|first|attr('name') }}</span>
                                {% endif %}
                                <span class="priority-badge priority-{{ todo.priority }}">{{ todo.priority.title() }}</span>
                            </div>
                        </div>
                        
                        {% if todo.description %}
                        <p style="margin: 10px 0; color: #666;">{{ todo.description }}</p>
                        {% endif %}
                        
                        <div class="todo-meta">
                            <div>Created: {{ todo.created_at }}</div>
                            {% if todo.due_date %}
                            <div class="due-date {% if todo.due_date < now and not todo.completed %}overdue{% elif todo.due_date.date() == now.date() %}today{% else %}future{% endif %}">
                                Due: {{ todo.due_date.strftime('%Y-%m-%d %H:%M') if todo.due_date else 'No due date' }}
                            </div>
                            {% endif %}
                            {% if todo.completed %}
                            <div>Completed: {{ todo.completed_at }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="todo-actions">
                            {% if not todo.completed %}
                            <a href="/complete/{{ todo.id }}" class="btn btn-success">✓ Complete</a>
                            {% endif %}
                            <a href="/delete/{{ todo.id }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this todo?')">🗑️ Delete</a>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty-state">
                        <h3>No todos yet!</h3>
                        <p>Add your first todo above to get started.</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        function filterTodos(filter) {
            const todos = document.querySelectorAll('.todo-item');
            const filterBtns = document.querySelectorAll('.filter-btn');
            
            // Update active button
            filterBtns.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            todos.forEach(todo => {
                const priority = todo.dataset.priority;
                const status = todo.dataset.status;
                let show = false;
                
                switch(filter) {
                    case 'all':
                        show = true;
                        break;
                    case 'active':
                        show = status === 'active';
                        break;
                    case 'completed':
                        show = status === 'completed';
                        break;
                    case 'high':
                        show = priority === 'high';
                        break;
                    case 'overdue':
                        // This would need server-side logic for proper overdue detection
                        show = true; // Simplified for demo
                        break;
                }
                
                todo.style.display = show ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main todo app page"""
    now = datetime.now()
    return render_template_string(HTML_TEMPLATE, todos=todos, categories=categories, now=now)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo with enhanced features"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium')
    category = request.form.get('category', '')
    due_date_str = request.form.get('due_date', '')
    
    if not title:
        flash('Title is required!', 'error')
        return redirect('/')
    
    # Parse due date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str.replace('T', ' '))
        except ValueError:
            flash('Invalid due date format!', 'error')
            return redirect('/')
    
    todo = {
        'id': str(uuid.uuid4()),
        'title': title,
        'description': description,
        'priority': priority,
        'category': category,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'completed_at': None,
        'due_date': due_date
    }
    
    todos.append(todo)
    flash(f'Todo "{title}" added successfully!', 'success')
    return redirect('/')

@app.route('/complete/<todo_id>')
def complete_todo(todo_id):
    """Mark a todo as completed"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            flash(f'Todo "{todo["title"]}" marked as completed!', 'success')
            break
    return redirect('/')

@app.route('/delete/<todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    original_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    
    if len(todos) < original_length:
        flash('Todo deleted successfully!', 'success')
    else:
        flash('Todo not found!', 'error')
    
    return redirect('/')

@app.route('/api/todos')
def api_todos():
    """API endpoint to get all todos"""
    return jsonify({
        "todos": todos,
        "total": len(todos),
        "active": len([t for t in todos if not t['completed']]),
        "completed": len([t for t in todos if t['completed']]),
        "timestamp": datetime.now().isoformat()
    })

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

@app.route('/api/todos/overdue')
def api_overdue_todos():
    """API endpoint to get overdue todos"""
    now = datetime.now()
    overdue_todos = [
        todo for todo in todos 
        if not todo['completed'] and todo.get('due_date') and todo['due_date'] < now
    ]
    return jsonify(overdue_todos)

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

@app.route('/api/categories')
def api_categories():
    """API endpoint to get all categories"""
    return jsonify(categories)

@app.route('/api/stats')
def api_stats():
    """API endpoint to get todo statistics"""
    now = datetime.now()
    active_todos = [t for t in todos if not t['completed']]
    completed_todos = [t for t in todos if t['completed']]
    high_priority = [t for t in todos if t['priority'] == 'high']
    overdue_todos = [
        t for t in todos 
        if not t['completed'] and t.get('due_date') and t['due_date'] < now
    ]
    
    return jsonify({
        "total": len(todos),
        "active": len(active_todos),
        "completed": len(completed_todos),
        "high_priority": len(high_priority),
        "overdue": len(overdue_todos),
        "completion_rate": (len(completed_todos) / len(todos) * 100) if todos else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 