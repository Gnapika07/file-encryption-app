%%writefile streamlit_app.py
import streamlit as st
from cryptography.fernet import Fernet

# Function to generate and save a key
def write_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a file
def encrypt_file(file):
    key = load_key()
    f = Fernet(key)
    data = file.read()
    encrypted = f.encrypt(data)
    return encrypted

# Decrypt a file
def decrypt_file(file):
    key = load_key()
    f = Fernet(key)
    encrypted_data = file.read()
    decrypted = f.decrypt(encrypted_data)
    return decrypted

# Streamlit UI
st.title("🔐 File Encryption and Decryption App")

option = st.selectbox("Choose an option:", ["Encrypt a File", "Decrypt a File"])

if option == "Encrypt a File":
    uploaded_file = st.file_uploader("Upload a file to encrypt", type=None)
    if uploaded_file:
        if st.button("Encrypt"):
            write_key()  # create a new key each time for simplicity
            encrypted_data = encrypt_file(uploaded_file)
            st.success("File encrypted successfully!")
            st.download_button("Download Encrypted File", encrypted_data, file_name="encrypted_file")

elif option == "Decrypt a File":
    uploaded_file = st.file_uploader("Upload an encrypted file", type=None)
    key_file = st.file_uploader("Upload the corresponding secret.key", type=["key"])
    if uploaded_file and key_file:
        # Save uploaded key
        with open("secret.key", "wb") as f:
            f.write(key_file.read())
        if st.button("Decrypt"):
            decrypted_data = decrypt_file(uploaded_file)
            st.success("File decrypted successfully!")
            st.download_button("Download Decrypted File", decrypted_data, file_name="decrypted_file.txt")
