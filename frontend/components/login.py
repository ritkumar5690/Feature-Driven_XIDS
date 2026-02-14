"""
Login Component for XIDS Frontend
Handles user authentication with email/username and password
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Simple user database (in production, this would be a proper database)
USERS_DB_FILE = os.path.join(os.path.dirname(__file__), "..", ".users.json")


def init_default_users():
    """Initialize default users if database doesn't exist"""
    if not os.path.exists(USERS_DB_FILE):
        os.makedirs(os.path.dirname(USERS_DB_FILE), exist_ok=True)
        demo_users = {
            "demo@xids.local": {
                "username": "demo_user",
                "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
        }
        with open(USERS_DB_FILE, 'w') as f:
            json.dump(demo_users, f, indent=2)


def load_users_db():
    """Load user database from JSON file"""
    init_default_users()
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users_db(users_db):
    """Save user database to JSON file"""
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(users_db, f, indent=2)


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email: str, username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user
    
    Args:
        email: User email
        username: Username
        password: User password
        
    Returns:
        Tuple of (success, message)
    """
    users_db = load_users_db()
    
    # Check if user already exists
    if email in users_db or any(u.get("username") == username for u in users_db.values()):
        return False, "User with this email or username already exists"
    
    # Validate inputs
    if not email or not username or not password:
        return False, "All fields are required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if "@" not in email:
        return False, "Invalid email format"
    
    # Create new user
    users_db[email] = {
        "username": username,
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users_db(users_db)
    logger.info(f"New user registered: {email}")
    return True, "Registration successful! Please login."


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    """
    Authenticate user with email and password
    
    Args:
        email: User email
        password: User password
        
    Returns:
        Tuple of (success, message)
    """
    users_db = load_users_db()
    
    if email not in users_db:
        return False, "Invalid email or password"
    
    user = users_db[email]
    if user["password_hash"] != hash_password(password):
        return False, "Invalid email or password"
    
    # Update last login
    user["last_login"] = datetime.now().isoformat()
    save_users_db(users_db)
    logger.info(f"User logged in: {email}")
    
    return True, "Login successful"


def render_login_page():
    """
    Render the login page with registration and login forms
    """
    st.set_page_config(
        page_title="XIDS - Login",
        page_icon="🛡️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for login page - Cybersecurity theme
    st.markdown("""
    <style>
        body {
            background-color: #0D1117;
            color: #E8E8E8;
        }
        
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #0D1117;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-header h1 {
            color: #00FF41;
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        
        .login-header p {
            color: #00CED1;
            font-size: 1rem;
            margin: 0.5rem 0 0 0;
            text-shadow: 0 0 10px rgba(0, 206, 209, 0.3);
        }
        
        .tab-content {
            background: #1A1F2E;
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #00CED1;
            box-shadow: 0 0 20px rgba(0, 206, 209, 0.3);
            color: #E8E8E8;
        }
        
        .form-divider {
            text-align: center;
            color: #00CED1;
            margin: 2rem 0;
            position: relative;
        }
        
        .form-divider::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #00FF41 0%, #00CED1 50%, #00FF41 100%);
        }
        
        .form-divider span {
            background: #1A1F2E;
            padding: 0 0.5rem;
            position: relative;
            color: #00FF41;
        }
        
        .success-message {
            background: #1A1F2E;
            color: #00FF41;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            border: 2px solid #00FF41;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.4);
        }
        
        .error-message {
            background: #1A1F2E;
            color: #FF1744;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            border: 2px solid #FF1744;
            box-shadow: 0 0 10px rgba(255, 23, 68, 0.4);
        }
        
        /* Input fields styling */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            background-color: #16202E;
            color: #00FF41;
            border: 2px solid #00CED1;
            border-radius: 5px;
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus {
            border-color: #00FF41;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
            color: #010409;
            border: 2px solid #00FF41;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        }
        
        .stButton>button:hover {
            box-shadow: 0 0 25px rgba(0, 255, 65, 0.8);
            transform: translateY(-2px);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab"] {
            background-color: #16202E;
            border: 2px solid #00CED1;
            color: #A0A0A0;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
            color: #010409;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='login-header'>
            <h1>🛡️ XIDS</h1>
            <p>Explainable Intrusion Detection System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for login and registration
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.markdown("### Sign In to Your Account")
                
                email = st.text_input(
                    "Email Address",
                    placeholder="you@example.com",
                    help="Enter your registered email address"
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    help="Enter your password"
                )
                
                submit_button = st.form_submit_button(
                    "🔓 Sign In",
                    width='stretch',
                    type="primary"
                )
                
                if submit_button:
                    if email and password:
                        success, message = authenticate_user(email, password)
                        if success:
                            st.session_state['authenticated'] = True
                            st.session_state['user_email'] = email
                            st.session_state['username'] = load_users_db()[email]["username"]
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter both email and password")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional info
            st.markdown("""
            <div style='margin-top: 1.5rem; text-align: center; color: #00CED1; font-size: 0.9rem;'>
                <p>Don't have an account? Switch to the <b style="color: #00FF41;">Register</b> tab</p>
                <p style='margin-top: 1rem;'>
                    <i style="color: #00FF41;">Default Demo Credentials:</i><br>
                    Email: <code style="color: #00FF41; background: #16202E; padding: 2px 5px; border-radius: 3px;">demo@xids.local</code><br>
                    Password: <code style="color: #00FF41; background: #16202E; padding: 2px 5px; border-radius: 3px;">demo123</code>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
            
            with st.form("register_form"):
                st.markdown("### Create New Account")
                
                email = st.text_input(
                    "Email Address",
                    placeholder="you@example.com",
                    help="Enter a valid email address"
                )
                username = st.text_input(
                    "Username",
                    placeholder="Choose a username",
                    help="Create a unique username"
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="At least 6 characters",
                    help="Password must be at least 6 characters"
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                    help="Confirm your password"
                )
                
                submit_button = st.form_submit_button(
                    "📝 Create Account",
                    width='stretch',
                    type="primary"
                )
                
                if submit_button:
                    if not all([email, username, password, confirm_password]):
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(email, username, password)
                        if success:
                            st.success(message)
                            st.info("You can now login with your credentials in the Login tab")
                        else:
                            st.error(message)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='margin-top: 1.5rem; text-align: center; color: #666; font-size: 0.9rem;'>
                <p>Already have an account? Switch to the <b>Login</b> tab</p>
            </div>
            """, unsafe_allow_html=True)


def check_authentication():
    """
    Check if user is authenticated
    
    Returns:
        True if authenticated, False otherwise
    """
    return st.session_state.get('authenticated', False)


def logout():
    """Logout the current user"""
    st.session_state['authenticated'] = False
    st.session_state['user_email'] = None
    st.session_state['username'] = None
    logger.info(f"User logged out: {st.session_state.get('user_email')}")


def get_current_user():
    """Get current authenticated user"""
    if check_authentication():
        return {
            "email": st.session_state.get('user_email'),
            "username": st.session_state.get('username')
        }
    return None