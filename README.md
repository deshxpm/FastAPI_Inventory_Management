# Project Overview
# Project Name: FastAPI Inventory Management

# Description:
FastAPI Inventory Management is a modern web application built using FastAPI, designed to manage and track items in an inventory. The application provides a RESTful API with endpoints to create, read, update, and delete items. It also includes user authentication and authorization features, allowing secure access to different functionalities based on user roles. The application leverages SQLAlchemy for database interactions and uses Jinja2 for rendering dynamic HTML pages.

# Features
# User Authentication

Signup: Users can register by providing a username, email, and password. Passwords are securely hashed using bcrypt.
Login: Authenticated users receive a JWT token that grants access to protected routes. The token is stored on the client side and used for subsequent requests.
Logout: Users can log out, which invalidates their session.

# Item Management
Create Item: Users can add new items to the inventory by providing item details such as name, description, and price.
Read Items: The application supports listing all items with pagination. Users can view individual item details.
Update Item: Users can modify existing items' details.
Delete Item: Users can remove items from the inventory.

# Templates and Static Files
Templates: Jinja2 templates are used for rendering HTML pages. The application includes pages for item listing, item creation, item updates, and user authentication.
Static Files: The application serves static files such as CSS, JavaScript, and images, enhancing the user interface.

# Endpoints
# User Endpoints
POST /signup: Register a new user.
POST /login: Authenticate a user and return a JWT token.
GET /logout: Logout the current user.

# Item Endpoints
POST /items/: Create a new item.
GET /items/: List all items with pagination.
GET /items/{item_id}: Retrieve details of a specific item.
PUT /items/{item_id}: Update an existing item.
DELETE /items/{item_id}: Delete a specific item.

# Technical Stack
Backend Framework: FastAPI
Database: SQLAlchemy with PostgreSQL
Authentication: JWT (JSON Web Tokens) for secure user authentication
Password Hashing: bcrypt via passlib
Templating: Jinja2
Static File Serving: FastAPI's StaticFiles
Environment Management: dotenv for environment variable management
Development
Installation

Create a virtual environment and install the required packages using pip.
Configuration

Set up environment variables, including the SECRET_KEY for JWT encoding/decoding.
Database Setup

Use SQLAlchemy to manage the database schema and migrations.
Running the Application

Start the FastAPI server and access the application through the provided endpoints.
# Testing
Ensure the application works as expected by testing the API endpoints and user authentication flows.
