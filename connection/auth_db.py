import sqlite3 as sq
import hashlib as ha
import streamlit as st
import pandas as pd
def init_db() :
    conn =sq.connect("user.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT DEFAULT 'user'
        )''')
    conn.commit()
    conn.close()
def hash_password(password):
    return ha.sha256(password.encode()).hexdigest()    

def verification_user(username, password):
    conn = sq.connect("user.db")
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    return user  # returns (username, role) or None
def afficher() :
    conn =sq.connect("user.db")
    cursor =conn.cursor()
    requete=cursor.execute('''select * from users''')
    requete=requete.fetchall()
    return requete
def ajout_user(username, password, role='user'):
    conn = sq.connect("user.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hash_password(password), role))
        conn.commit()
    except sq.IntegrityError:
        return False
    finally:
        conn.close()
    return True
def login():
   
    st.session_state.authenticated = False
    st.title("🔐 Connexion")
    with st.form("form1") :
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        bouton =st.form_submit_button("Se connecter")
        if bouton:
            user = verification_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = user[0]
                st.session_state.role = user[1]
                st.success(f"Bienvenue {user[0]} ({user[1]}) ✅")
            else:
                st.error("Identifiants incorrects ❌")
    st.markdown("")
    st.subheader("Créer un compte")
    with st.form("form2") :
        new_user = st.text_input("Nouvel utilisateur")
        new_pass = st.text_input("Mot de passe pour le nouveau compte", type="password")
        role = st.selectbox("Rôle", ["user", "admin"])
        bouton =st.form_submit_button("Créer un compte") 
        if bouton:
            if ajout_user(new_user, new_pass, role):
                st.success("Utilisateur créé avec succès ✅")
            else:
                st.error("Ce nom d'utilisateur existe déjà ❌")
     