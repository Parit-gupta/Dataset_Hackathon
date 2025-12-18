import bcrypt
import sqlite3

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# ---------------- PASSWORD UTILS ----------------
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)


# ---------------- USER OPERATIONS ----------------
def add_user(username: str, email: str, password: str) -> bool:
    """
    Adds a new user to the database.
    Returns True if successful, False otherwise.
    """
    if not username or not email or not password:
        return False

    try:
        c.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (
                username.strip(),
                email.strip().lower(),
                hash_password(password),
            ),
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # Email already exists
        return False

    except Exception:
        return False


def login_user(email: str, password: str) -> bool:
    """
    Verifies user credentials.
    Returns True if login is successful, else False.
    """
    if not email or not password:
        return False

    c.execute(
        "SELECT password FROM users WHERE email = ?",
        (email.strip().lower(),),
    )
    result = c.fetchone()

    if result and check_password(password, result[0]):
        return True

    return False
