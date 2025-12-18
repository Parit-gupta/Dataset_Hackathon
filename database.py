"""
Database Module for GenAI Big Data Platform
Handles all database operations for users and assessments
"""

import json
import os
import hashlib
from datetime import datetime

# File paths
USERS_FILE = "users.json"
ASSESSMENTS_FILE = "assessments/assessments.json"

def hash_password(password):
    """
    Hash password using SHA-256
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """
    Load users from JSON file
    
    Returns:
        dict: Dictionary of users
    """
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """
    Save users to JSON file
    
    Args:
        users (dict): Dictionary of users to save
    """
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def user_exists(email):
    """
    Check if user exists by email
    
    Args:
        email (str): Email to check
        
    Returns:
        bool: True if user exists
    """
    users = load_users()
    return email in users

def register_user(username, email, password, role):
    """
    Register a new user
    
    Args:
        username (str): User's display name
        email (str): User's email
        password (str): User's password (will be hashed)
        role (str): User role ('teacher' or 'student')
        
    Returns:
        bool: True if registration successful
    """
    users = load_users()
    
    if email in users:
        return False
    
    users[email] = {
        'username': username,
        'email': email,
        'password': hash_password(password),
        'role': role,
        'created_at': datetime.now().isoformat(),
        'assessments_taken': [],
        'assessments_created': [] if role == 'teacher' else None
    }
    
    save_users(users)
    return True

def verify_user(email, password):
    """
    Verify user credentials
    
    Args:
        email (str): User's email
        password (str): User's password
        
    Returns:
        bool: True if credentials are valid
    """
    users = load_users()
    
    if email not in users:
        return False
    
    return users[email]['password'] == hash_password(password)

def get_user_by_email(email):
    """
    Get user data by email
    
    Args:
        email (str): User's email
        
    Returns:
        dict: User data or None
    """
    users = load_users()
    
    if email not in users:
        return None
    
    user = users[email].copy()
    # Don't return password
    user.pop('password', None)
    return user

def get_user_role(email):
    """
    Get user's role
    
    Args:
        email (str): User's email
        
    Returns:
        str: User's role or None
    """
    users = load_users()
    
    if email not in users:
        return None
    
    return users[email].get('role')

def update_user(email, updates):
    """
    Update user data
    
    Args:
        email (str): User's email
        updates (dict): Dictionary of fields to update
        
    Returns:
        bool: True if update successful
    """
    users = load_users()
    
    if email not in users:
        return False
    
    for key, value in updates.items():
        if key != 'password' and key != 'email':  # Don't allow direct password/email updates
            users[email][key] = value
    
    save_users(users)
    return True

def add_assessment_to_user(email, assessment_id):
    """
    Add assessment to user's taken list
    
    Args:
        email (str): User's email
        assessment_id (str): Assessment ID
        
    Returns:
        bool: True if successful
    """
    users = load_users()
    
    if email not in users:
        return False
    
    if 'assessments_taken' not in users[email]:
        users[email]['assessments_taken'] = []
    
    if assessment_id not in users[email]['assessments_taken']:
        users[email]['assessments_taken'].append(assessment_id)
    
    save_users(users)
    return True

def get_user_assessments(email):
    """
    Get list of assessments taken by user
    
    Args:
        email (str): User's email
        
    Returns:
        list: List of assessment IDs
    """
    users = load_users()
    
    if email not in users:
        return []
    
    return users[email].get('assessments_taken', [])

def get_all_users():
    """
    Get all users (without passwords)
    
    Returns:
        dict: Dictionary of all users
    """
    users = load_users()
    
    # Remove passwords from response
    safe_users = {}
    for email, data in users.items():
        safe_users[email] = data.copy()
        safe_users[email].pop('password', None)
    
    return safe_users

def get_users_by_role(role):
    """
    Get all users with specific role
    
    Args:
        role (str): Role to filter by
        
    Returns:
        dict: Dictionary of users with that role
    """
    users = load_users()
    
    filtered_users = {}
    for email, data in users.items():
        if data.get('role') == role:
            filtered_users[email] = data.copy()
            filtered_users[email].pop('password', None)
    
    return filtered_users

def delete_user(email):
    """
    Delete a user
    
    Args:
        email (str): User's email
        
    Returns:
        bool: True if deletion successful
    """
    users = load_users()
    
    if email not in users:
        return False
    
    del users[email]
    save_users(users)
    return True

def change_password(email, old_password, new_password):
    """
    Change user's password
    
    Args:
        email (str): User's email
        old_password (str): Current password
        new_password (str): New password
        
    Returns:
        bool: True if password changed successfully
    """
    users = load_users()
    
    if email not in users:
        return False
    
    if users[email]['password'] != hash_password(old_password):
        return False
    
    users[email]['password'] = hash_password(new_password)
    save_users(users)
    return True