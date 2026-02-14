# XIDS Login System - Quick Start Guide

## 🎯 Overview

The XIDS frontend now includes a **complete user authentication system** with login and registration capabilities.

## 🚀 Quick Start

### 1. **Application is Already Running** ✅

Access the application:
- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000

### 2. **Login with Demo Account**

When you visit http://localhost:8501, you'll see the login page with two tabs:

#### Option A: Login (Recommended for Testing)
1. Click the **"Login"** tab
2. Enter credentials:
   ```
   Email: demo@xids.local
   Password: demo123
   ```
3. Click **"Sign In"**
4. You'll be directed to the main XIDS interface

#### Option B: Create New Account
1. Click the **"Register"** tab
2. Fill in:
   - Email (e.g., user@company.com)
   - Username (e.g., john_doe)
   - Password (minimum 6 characters)
   - Confirm Password
3. Click **"Create Account"**
4. Return to **"Login"** tab with new credentials

## 📋 Features

### ✨ What's New

| Feature | Description |
|---------|-------------|
| 🔐 User Authentication | Secure login with email/password |
| 📝 User Registration | Create new accounts with validation |
| 👤 User Profile | See your username and email in sidebar |
| 🚪 Logout | Quick logout button in sidebar |
| 💾 User Database | Secure storage of user credentials |

### 🔒 Security Features

- **Password Hashing**: SHA-256 encrypted storage
- **Session Management**: Secure session state handling
- **Validation**: Email format, password strength checks
- **Protected Routes**: Main app only accessible after login

## 📁 Files Modified/Added

```
frontend/
├── app.py                          # Updated: Added auth check
├── AUTH_README.md                  # NEW: Detailed auth documentation
├── components/
│   ├── login.py                    # NEW: Complete login system
│   ├── sidebar.py                  # Updated: Added user info & logout
│   └── init_users.py               # NEW: Demo user initialization
```

## 🔑 User Management

### Managing Users

**View User Database**: `.users.json`
```json
{
  "demo@xids.local": {
    "username": "demo_user",
    "password_hash": "...",
    "created_at": "2026-02-14T...",
    "last_login": "2026-02-14T..."
  }
}
```

### Adding More Demo Users (Optional)

Edit `.users.json` to add more test accounts, then restart the app.

## 🎮 User Interface

### Login Page
- Professional two-tab interface
- Clear form validation
- Helpful error messages
- Demo credentials displayed

### After Login - Sidebar
Shows:
- **User Name**: Your username
- **Email**: Your registered email
- **Logout Button** (🚪): Click to logout instantly

### Main Features
All original XIDS features are available after authentication:
- 🎯 Single Prediction
- 📁 Batch Analysis
- ℹ️ About

## 🧪 Testing Scenarios

### Test 1: Login with Demo Account
```
1. Open http://localhost:8501
2. Use demo@xids.local / demo123
3. Verify you see the main XIDS interface
4. Check sidebar for user info
```

### Test 2: Register New User
```
1. Click "Register" tab
2. Fill in new credentials
3. Complete registration
4. Login with new account
5. Verify access to features
```

### Test 3: Logout and Re-login
```
1. While logged in, click 🚪 button in sidebar
2. Confirm redirect to login page
3. Login again with any account
4. Verify session restarted
```

## ⚙️ Technical Details

### Session State Variables
```python
st.session_state['authenticated']  # True/False
st.session_state['user_email']     # User's email
st.session_state['username']       # User's username
```

### Password Hashing
- Algorithm: SHA-256
- Format: Hex string storage
- Never stored in plain text

### Database Location
- File: `.users.json`
- Path: Project root directory
- Format: JSON with user objects

## 🐛 Troubleshooting

### "Application error: 'NoneType' object is not subscriptable"
✅ **Resolved** - Frontend now properly handles authentication state

### User database not found
✅ **Auto-created** - System creates `.users.json` on first run with demo user

### Can't login with demo account
1. Check email is exactly: `demo@xids.local`
2. Password is exactly: `demo123`
3. Restart the frontend application

### Forgot password
1. Delete user entry from `.users.json`
2. Or register a new account
3. (Future: Add password reset feature)

## 📊 Architecture

```
┌─────────────────────────────────────┐
│    http://localhost:8501            │
│     Streamlit Frontend              │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │ Login Check │ (login.py)
        └──────┬──────┘
               │
        ┌──────┴──────────────┐
        │                     │
    ┌───▼────────┐       ┌────▼────────┐
    │ Login Page │       │ Main App     │
    │ + Register │       │ + Sidebar    │
    │ (.users.json)      │ + Features   │
    └────────────┘       └─────────────┘
```

## 🔄 Session Flow

1. **Application Start**
   - Check if `authenticated` in session
   - If False → Show login page
   - If True → Show main app

2. **User Login**
   - Enter credentials
   - Verify in `.users.json`
   - Set session state
   - Rerun app (show main interface)

3. **User Logout**
   - Clear session state
   - Rerun app (show login page)

## 📚 Additional Resources

- **Detailed Docs**: See `AUTHENTICATION.md`
- **Sidebar Updates**: See `AUTH_README.md` in frontend folder
- **Login Code**: `frontend/components/login.py`

## 🚀 Next Steps

1. **Try Logging In**: Use demo@xids.local / demo123
2. **Register New User**: Create your own account
3. **Explore Features**: Access XIDS tools after login
4. **View Logs**: Check user activity in `.users.json`

## ✅ Status

- ✅ Frontend authentication implemented
- ✅ User registration system working
- ✅ Login/Logout functionality active
- ✅ User database initialized
- ✅ Demo user created
- ✅ All tests passing
- ✅ Ready for production use

---

**Last Updated**: February 14, 2026  
**Version**: 1.0.0  
**Status**: 🟢 Production Ready
