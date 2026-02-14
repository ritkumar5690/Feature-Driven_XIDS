"""
Initialize demo user for XIDS application
"""

import json
import hashlib
import os
from datetime import datetime


def init_demo_user():
    """Create a demo user for testing"""
    users_db_file = os.path.join(os.path.dirname(__file__), "..", ".users.json")
    
    # Create users database with demo user
    demo_users = {
        "demo@xids.local": {
            "username": "demo_user",
            "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
    }
    
    # Only create if doesn't exist
    if not os.path.exists(users_db_file):
        os.makedirs(os.path.dirname(users_db_file), exist_ok=True)
        with open(users_db_file, 'w') as f:
            json.dump(demo_users, f, indent=2)
        print(f"Demo user created at {users_db_file}")
        print("Demo credentials:")
        print("  Email: demo@xids.local")
        print("  Password: demo123")
    else:
        print(f"Users database already exists at {users_db_file}")


if __name__ == "__main__":
    init_demo_user()
