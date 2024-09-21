import streamlit as st
import sqlite3
import bcrypt

# Database initialization
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user
def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()

# Function to check user credentials
def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False

# Initialize the database
init_db()

# Set up Streamlit interface
st.set_page_config(page_title="Sellorita - Your AI Marketing Assistant", page_icon="💡", layout="wide")

st.title("Welcome to Sellorita AI 💡")

# Tabs for Login and Registration
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("User Login")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Login"):
        if check_user(username, password):
            st.success("Login successful!")
            # Proceed to main application
        else:
            st.error("Invalid username or password.")

with tab2:
    st.subheader("User Registration")
    new_username = st.text_input("New Username", placeholder="Choose a username")
    new_password = st.text_input("New Password", placeholder="Choose a password", type="password")

    if st.button("Register"):
        if new_username and new_password:
            try:
                add_user(new_username, new_password)
                st.success(f'User {new_username} registered successfully!')
            except sqlite3.IntegrityError:
                st.error('Username already exists. Please choose a different one.')
        else:
            st.error('Please fill in all fields.')

st.markdown("""
### About Sellorita
Sellorita is designed to empower your marketing strategies with AI-driven insights and creative solutions. Our vision is to simplify marketing for everyone, making it accessible and effective.

For any inquiries, please contact us at: support@sellorita.com
""")
