import streamlit as st
import hashlib
from cryptography.fernet import Fernet

st.set_page_config(page_title="Secure Data Encryption System",page_icon="🔐",layout="centered")


KEY = Fernet.generate_key()
cipher = Fernet(KEY)

stored_data = {}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    if encrypted_text in stored_data and stored_data[encrypted_text]["passkey"] == hashed_passkey:
        st.session_state.failed_attempts = 0
        return cipher.decrypt(encrypted_text.encode()).decode()
    else:
        st.session_state.failed_attempts += 1
        return None

st.title("🔒 Secure Data Encryption System")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

# ---------------- Home Page ----------------
if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.write("""
    Use this tool to:
    - 🔐 Securely store data with encryption
    - 🔍 Retrieve data with a unique passkey
    - 🔁 Auto-lock after 3 failed decryption attempts
    """)

# ---------------- Store Data ----------------
elif choice == "Store Data":
    st.subheader("📂 Store Your Secure Data")
    user_text = st.text_area("Enter your data:")
    passkey = st.text_input("Enter a secret passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_text and passkey:
            encrypted_text = encrypt_data(user_text)
            hashed_passkey = hash_passkey(passkey)
            stored_data[encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
            st.success("✅ Your data has been encrypted and stored securely!")
            st.code(encrypted_text, language='text')
        else:
            st.error("⚠️ Please fill in both fields.")

# ---------------- Retrieve Data ----------------
elif choice == "Retrieve Data":
    if st.session_state.failed_attempts >= 3:
        st.warning("🔒 Too many failed attempts. Please reauthorize.")
        st.switch_page("Login")

    st.subheader("🔍 Retrieve Your Data")
    encrypted_input = st.text_area("Paste your encrypted data:")
    passkey = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            result = decrypt_data(encrypted_input, passkey)
            if result:
                st.success("✅ Decryption Successful!")
                st.text_area("Your Decrypted Data:", result, height=150)
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Lock triggered! Please log in again.")
                    st.switch_page("Login")
        else:
            st.error("⚠️ Please enter both fields.")

# ---------------- Login Page ----------------
elif choice == "Login":
    st.subheader("🔐 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Replace with secure method
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized. You can now try again.")
        else:
            st.error("❌ Incorrect master password.")