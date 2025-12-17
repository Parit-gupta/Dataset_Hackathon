import streamlit as st
import pandas as pd
from auth import add_user, login_user
import database  # init DB

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "auth_stage" not in st.session_state:
    st.session_state.auth_stage = None
    # None | "signup" | "login" | "signup_success"

# ---------------- PAGE CONFIG ----------------
st.set_page_config("GenAI Big Data Platform", "📊", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(to right, #f8fafc, #eef2ff); }
.title { font-size: 34px; font-weight: 800; }
.card {
    background: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
}
.stButton > button {
    border-radius: 25px;
    font-weight: 600;
}
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
l, r = st.columns([8, 2])

with l:
    st.markdown('<div class="title">🚀 GenAI Big Data Platform</div>', unsafe_allow_html=True)

with r:
    if not st.session_state.logged_in:
        if st.button("Login", key="top_login"):
            st.session_state.auth_stage = "login"
        if st.button("Signup", key="top_signup"):
            st.session_state.auth_stage = "signup"
    else:
        with st.popover("👤"):
            st.write(f"**Email:** {st.session_state.user_email}")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.auth_stage = None
                st.rerun()

st.divider()

# ---------------- DATASET UPLOAD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📤 Upload Dataset")

if not st.session_state.logged_in:
    st.info("🔒 Login required to upload datasets")
    uploaded_file = None
else:
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- AUTH SECTION ----------------
if st.session_state.auth_stage and not st.session_state.logged_in:

    st.divider()
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ---------- SIGNUP ----------
    if st.session_state.auth_stage == "signup":
        st.subheader("📝 Create Account")

        username = st.text_input("Username", key="su_user")
        email = st.text_input("Email", key="su_email")
        password = st.text_input("Password", type="password", key="su_pass")

        if st.button("Create Account"):
            if add_user(username, email, password):
                st.session_state.auth_stage = "signup_success"
                st.rerun()
            else:
                st.error("Invalid details or user already exists")

        st.markdown("---")
        if st.button("Already have an account? Login"):
            st.session_state.auth_stage = "login"
            st.rerun()

    # ---------- SIGNUP SUCCESS ----------
    elif st.session_state.auth_stage == "signup_success":
        st.success("🎉 Account created successfully!")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Go to Login"):
            st.session_state.auth_stage = "login"
            st.rerun()

    # ---------- LOGIN ----------
    elif st.session_state.auth_stage == "login":
        st.subheader("🔐 Login")

        email = st.text_input("Email", key="li_email")
        password = st.text_input("Password", type="password", key="li_pass")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.auth_stage = None
                st.success("Login successful 🎉")
                st.rerun()
            else:
                st.error("Invalid email or password")

        st.markdown("---")
        if st.button("New here? Create an account"):
            st.session_state.auth_stage = "signup"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- POST LOGIN VIEW ----------------
if uploaded_file and st.session_state.logged_in:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset uploaded successfully!")
    st.dataframe(df.head())

# ---------------- INFO SECTION ----------------
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
        <h3>💡 About</h3>
        <ul>
            <li>GenAI-powered analytics</li>
            <li>Big Data ready</li>
            <li>Secure authentication</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>⚙️ How It Works</h3>
        <ol>
            <li>Explore freely</li>
            <li>Create account / Login</li>
            <li>Upload dataset</li>
            <li>Analyze data</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
