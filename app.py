from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
DEBUG_MODE = os.getenv('DEBUG', 'True').lower() == 'true'

# Sample data storage (in-memory for demo)
users = [
    {
        "id": "1",
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "2", 
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 25,
        "created_at": "2024-01-16T14:30:00Z"
    }
]

products = [
    {
        "id": "1",
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": "2",
        "name": "Coffee Mug",
        "price": 12.99,
        "category": "Kitchen",
        "in_stock": True
    }
]

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({
        "users": users,
        "total": len(users),
        "success": True
    })

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify({
            "user": user,
            "success": True
        })
    return jsonify({
        "error": "User not found",
        "success": False
    }), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({
            "error": "Name and email are required",
            "success": False
        }), 400
    
    # Check if email already exists
    if any(u['email'] == data['email'] for u in users):
        return jsonify({
            "error": "Email already exists",
            "success": False
        }), 400
    
    new_user = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age', 0),
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    
    return jsonify({
        "user": new_user,
        "message": "User created successfully",
        "success": True
    }), 201

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({
            "error": "User not found",
            "success": False
        }), 404
    
    data = request.get_json()
    
    if data.get('name'):
        user['name'] = data['name']
    if data.get('email'):
        user['email'] = data['email']
    if data.get('age') is not None:
        user['age'] = data['age']
    
    return jsonify({
        "user": user,
        "message": "User updated successfully",
        "success": True
    })

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    global users
    original_length = len(users)
    users = [u for u in users if u['id'] != user_id]
    
    if len(users) < original_length:
        return jsonify({
            "message": "User deleted successfully",
            "success": True
        })
    
    return jsonify({
        "error": "User not found",
        "success": False
    }), 404

# Product endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({
        "products": products,
        "total": len(products),
        "success": True
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify({
            "product": product,
            "success": True
        })
    return jsonify({
        "error": "Product not found",
        "success": False
    }), 404

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({
            "error": "Name and price are required",
            "success": False
        }), 400
    
    new_product = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "price": float(data['price']),
        "category": data.get('category', 'General'),
        "in_stock": data.get('in_stock', True)
    }
    
    products.append(new_product)
    
    return jsonify({
        "product": new_product,
        "message": "Product created successfully",
        "success": True
    }), 201

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({
            "error": "Product not found",
            "success": False
        }), 404
    
    data = request.get_json()
    
    if data.get('name'):
        product['name'] = data['name']
    if data.get('price') is not None:
        product['price'] = float(data['price'])
    if data.get('category'):
        product['category'] = data['category']
    if data.get('in_stock') is not None:
        product['in_stock'] = data['in_stock']
    
    return jsonify({
        "product": product,
        "message": "Product updated successfully",
        "success": True
    })

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    global products
    original_length = len(products)
    products = [p for p in products if p['id'] != product_id]
    
    if len(products) < original_length:
        return jsonify({
            "message": "Product deleted successfully",
            "success": True
        })
    
    return jsonify({
        "error": "Product not found",
        "success": False
    }), 404

# Search endpoints
@app.route('/api/search/users', methods=['GET'])
def search_users():
    """Search users by name or email"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({
            "users": users,
            "total": len(users),
            "success": True
        })
    
    filtered_users = [
        u for u in users 
        if query in u['name'].lower() or query in u['email'].lower()
    ]
    
    return jsonify({
        "users": filtered_users,
        "total": len(filtered_users),
        "query": query,
        "success": True
    })

@app.route('/api/search/products', methods=['GET'])
def search_products():
    """Search products by name or category"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({
            "products": products,
            "total": len(products),
            "success": True
        })
    
    filtered_products = [
        p for p in products 
        if query in p['name'].lower() or query in p['category'].lower()
    ]
    
    return jsonify({
        "products": filtered_products,
        "total": len(filtered_products),
        "query": query,
        "success": True
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "success": False
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "success": False
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0',
        port=port
    ) 