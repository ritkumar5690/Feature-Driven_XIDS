# XIDS Frontend Authentication

## Login-Based Protocol Implementation

The XIDS frontend now includes a complete authentication system with user registration and login capabilities.

## Features

### 1. **User Authentication**
   - Email/username and password-based login
   - User registration with validation
   - Secure password hashing (SHA-256)
   - Session state management

### 2. **Login Page**
   - Professional login interface with tabs
   - **Login Tab**: Sign in with existing credentials
   - **Register Tab**: Create new user accounts
   - Default demo user for testing

### 3. **User Management**
   - User information displayed in sidebar
   - Logout functionality with one-click button
   - User database stored locally in JSON format
   - Last login tracking

## Demo Credentials

Use these credentials to test the application:

```
Email: demo@xids.local
Password: demo123
```

## User Registration

1. Click on the **Register** tab on the login page
2. Enter your email address
3. Create a username
4. Set a password (minimum 6 characters)
5. Confirm your password
6. Click "Create Account"

## Components

### `components/login.py`
Contains all authentication logic:
- `render_login_page()`: Main login UI
- `authenticate_user()`: Validates user credentials
- `register_user()`: Creates new user accounts
- `check_authentication()`: Checks if user is logged in
- `logout()`: Logs out current user
- `get_current_user()`: Returns current user info

### Updated `components/sidebar.py`
Now includes:
- User information display
- Quick logout button
- User session details

### Updated `app.py`
Main app now:
- Checks authentication before showing main interface
- Shows login page if not authenticated
- Initializes session state for auth tracking

## User Database

User credentials are stored in `.users.json` file located at the project root level:

```
xids_project/
├── .users.json          # User database file
├── frontend/
│   └── components/
│       ├── login.py     # Login component
│       └── sidebar.py   # Updated sidebar
└── ...
```

### Database Format

```json
{
  "user@example.com": {
    "username": "username",
    "password_hash": "hashed_password",
    "created_at": "2026-02-14T...",
    "last_login": "2026-02-14T..."
  }
}
```

## Security Notes

- Passwords are hashed using SHA-256
- No plain text passwords are stored
- Session state is managed through Streamlit session management
- User emails are treated as unique identifiers

## File Locations

- **User Database**: `.users.json` (root level)
- **Login Component**: `frontend/components/login.py`
- **Sidebar Updates**: `frontend/components/sidebar.py`
- **Main App Updates**: `frontend/app.py`

## Password Requirements

- Minimum 6 characters
- Case-sensitive
- Must match confirmation during registration

## Usage Flow

1. **First Time**: Register a new account
2. **Login**: Use email and password to log in
3. **Access**: Once logged in, access all XIDS features
4. **Logout**: Click logout button in sidebar to exit

## Future Enhancements

For production deployment, consider:
- Database integration (PostgreSQL, MongoDB, etc.)
- Advanced password hashing (bcrypt, Argon2)
- Two-factor authentication (2FA)
- OAuth/SSO integration
- Token-based authentication (JWT)
- Rate limiting on login attempts
- Email verification for registration
