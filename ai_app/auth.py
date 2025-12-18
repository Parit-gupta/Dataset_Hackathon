import sqlite3
import hashlib
import os

# Database file path
DB_FILE = "users.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with users table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password, role='student'):
    """
    Add a new user to the database
    
    Returns:
        bool: True if user was added successfully, False otherwise
    """
    # Clean inputs
    username = username.strip() if username else ""
    email = email.strip().lower() if email else ""
    password = password.strip() if password else ""
    
    # Validate username
    if not username or len(username) < 2:
        print("Error: Username must be at least 2 characters")
        return False
    
    # Validate email
    if not email:
        print("Error: Email is required")
        return False
    
    if '@' not in email or '.' not in email.split('@')[-1]:
        print("Error: Invalid email format. Must contain @ and domain (e.g., user@example.com)")
        return False
    
    # Validate password
    if not password:
        print("Error: Password is required")
        return False
    
    if len(password) < 6:
        print("Error: Password must be at least 6 characters long")
        return False
    
    # Validate role
    if role not in ['student', 'teacher']:
        print("Error: Role must be 'student' or 'teacher'")
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"Error: An account with email '{email}' already exists")
            conn.close()
            return False
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, role))
        
        conn.commit()
        conn.close()
        
        print(f"✅ User '{username}' ({role}) created successfully!")
        return True
        
    except sqlite3.IntegrityError as e:
        print(f"Database error: Email already exists or constraint violation")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def login_user(email, password):
    """
    Authenticate a user and return their information
    
    Returns:
        dict: User information if authentication successful, None otherwise
    """
    # Clean inputs
    email = email.strip().lower() if email else ""
    password = password.strip() if password else ""
    
    # Validate inputs
    if not email:
        print("Error: Email is required")
        return None
    
    if not password:
        print("Error: Password is required")
        return None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the provided password
        password_hash = hash_password(password)
        
        # Query user with matching email and password
        cursor.execute('''
            SELECT id, username, email, role 
            FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_dict = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
            print(f"✅ Login successful for {user_dict['username']} ({user_dict['role']})")
            return user_dict
        else:
            print("❌ Invalid email or password")
            return None
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return None

def get_user_by_email(email):
    """Retrieve user information by email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, created_at
            FROM users 
            WHERE email = ?
        ''', (email.strip().lower(),))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at']
            }
        return None
        
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        return None

def update_user_role(email, new_role):
    """Update a user's role"""
    if new_role not in ['student', 'teacher']:
        print("Error: Role must be 'student' or 'teacher'")
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET role = ? 
            WHERE email = ?
        ''', (new_role, email.strip().lower()))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            print(f"✅ Role updated to {new_role} for {email}")
            return True
        else:
            print(f"❌ No user found with email {email}")
            return False
            
    except Exception as e:
        print(f"Error updating role: {str(e)}")
        return False

def delete_user(email):
    """Delete a user from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE email = ?', (email.strip().lower(),))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            print(f"✅ User {email} deleted successfully")
            return True
        else:
            print(f"❌ No user found with email {email}")
            return False
            
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return False

def get_all_users():
    """Retrieve all users from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, created_at
            FROM users
            ORDER BY created_at DESC
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at']
            }
            for user in users
        ]
        
    except Exception as e:
        print(f"Error retrieving users: {str(e)}")
        return []

def get_users_by_role(role):
    """Retrieve all users with a specific role"""
    if role not in ['student', 'teacher']:
        print("Error: Role must be 'student' or 'teacher'")
        return []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, role, created_at
            FROM users
            WHERE role = ?
            ORDER BY created_at DESC
        ''', (role,))
        
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at']
            }
            for user in users
        ]
        
    except Exception as e:
        print(f"Error retrieving users by role: {str(e)}")
        return []

def change_password(email, old_password, new_password):
    """Change a user's password"""
    if len(new_password.strip()) < 6:
        print("Error: New password must be at least 6 characters")
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        old_password_hash = hash_password(old_password.strip())
        cursor.execute('''
            SELECT id FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email.strip().lower(), old_password_hash))
        
        if not cursor.fetchone():
            print("Error: Invalid current password")
            conn.close()
            return False
        
        new_password_hash = hash_password(new_password.strip())
        cursor.execute('''
            UPDATE users 
            SET password_hash = ? 
            WHERE email = ?
        ''', (new_password_hash, email.strip().lower()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Password changed successfully for {email}")
        return True
        
    except Exception as e:
        print(f"Error changing password: {str(e)}")
        return False

# Initialize database when module is imported
init_database()

# Debugging utility - delete if user exists
def reset_user(email):
    """Debug function to delete a user if they exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE email = ?', (email.strip().lower(),))
        conn.commit()
        conn.close()
        return True
    except:
        return False

if __name__ == "__main__":
    print("Testing authentication module...")
    
    # Clean test data
    reset_user("john@example.com")
    reset_user("jane@teacher.com")
    
    print("\n--- Testing User Creation ---")
    add_user("John Doe", "john@example.com", "password123", "student")
    add_user("Jane Teacher", "jane@teacher.com", "teacher123", "teacher")
    
    print("\n--- Testing Login ---")
    user = login_user("john@example.com", "password123")
    if user:
        print(f"Logged in as: {user['username']} ({user['role']})")
    
    print("\n--- Testing Get All Users ---")
    all_users = get_all_users()
    print(f"Total users: {len(all_users)}")
    for u in all_users:
        print(f"  - {u['username']} ({u['email']}) - {u['role']}")