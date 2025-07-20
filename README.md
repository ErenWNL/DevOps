# Simple Flask API Backend

A simple REST API built with Flask for demonstration purposes.

## Features

- 🔍 **Health Check** - API status monitoring
- 👥 **User Management** - CRUD operations for users
- 📦 **Product Management** - CRUD operations for products
- 🔎 **Search Functionality** - Search users and products
- 🌐 **CORS Support** - Cross-origin resource sharing enabled
- 🔧 **Environment Configuration** - Configurable via .env file

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Users
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get specific user
- `POST /api/users` - Create new user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get specific product
- `POST /api/products` - Create new product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Search
- `GET /api/search/users?q={query}` - Search users
- `GET /api/search/products?q={query}` - Search products

## Example Usage

### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

### Get All Users
```bash
curl http://localhost:5000/api/users
```

### Create a Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "category": "Electronics"}'
```

### Search Products
```bash
curl "http://localhost:5000/api/search/products?q=laptop"
```

## Environment Variables

- `SECRET_KEY` - Flask secret key
- `DEBUG` - Enable/disable debug mode
- `PORT` - Port to run the server on

## Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── env.example        # Environment variables template
└── README.md          # This file
```

## Notes

- This is a demo application with in-memory data storage
- Data will be lost when the server restarts
- For production use, add a proper database
- Remember to change the SECRET_KEY in production 