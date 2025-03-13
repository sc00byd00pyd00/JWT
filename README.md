# JWT
## Flask JWT Authentication API
The Flask-based web application provides a JWT (JSON Web Token) authentication system, allowing users to log in, obtain access tokens, refresh tokens, and access protected resources. It includes role-based access control (RBAC), supporting both admin and user roles. Admins can manage users (add or delete them), while normal users can only authenticate and access protected routes.

### Key Features:
User Authentication: Users log in with a username and password to receive an access token and a refresh token.
JWT-based Authorization: Secure API endpoints using access tokens.
Token Refreshing: Users can request a new access token using the refresh token.
Protected Routes: Only authenticated users can access certain API endpoints.
Admin Controls: Admin users can add or delete other users.
Role-Based Access: Admin-only endpoints ensure non-admin users cannot perform administrative tasks.

## Bash Script for API Interaction
The Bash script provides a command-line interface (CLI) to interact with the Flask API using curl. It automates authentication and user management tasks without requiring manual API calls.

### Key Features:
Login Function: Prompts for a username and password, then retrieves access and refresh tokens.
Token Refreshing: Allows refreshing the access token when expired.
Access Protected Routes: Calls the API's protected endpoints.
User Management (Admin Only): Admin users can list, add, and delete users via the script.
Interactive Menu: Provides an easy-to-use menu for selecting API operations.
How They Work Together
The Flask API serves as the backend, handling authentication and user management.
The Bash script acts as a client, making API requests to authenticate users and interact with the system.
