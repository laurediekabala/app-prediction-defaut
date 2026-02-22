import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Supabase
@st.cache_resource
def init_connection():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("Veuillez configurer SUPABASE_URL et SUPABASE_KEY dans votre fichier .env")
        return None
    return create_client(url, key)

supabase: Client = init_connection()

def verification_user(email, password):
    """Connexion utilisateur avec Supabase Auth"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            return response.user
        return None
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None

def ajout_user(email, password):
    """Créer un nouveau compte utilisateur"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if response.user:
            return True
        return False
    except Exception as e:
        st.error(f"Erreur lors de la création du compte: {str(e)}")
        return False

def get_user_profile(user_id):
    """Récupérer le profil utilisateur depuis la table profile"""
    try:
        response = supabase.table("profile").select("*").eq("id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération du profil: {str(e)}")
        return None

def login():
    """Interface de connexion"""
    st.title("🔐 Connexion")
    
    tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])
    
    with tab1:
        st.subheader("Connexion")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            bouton = st.form_submit_button("Se connecter")
            
            if bouton:
                if email and password:
                    user = verification_user(email, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user.id
                        st.session_state.email = user.email
                        
                        # Récupérer le profil utilisateur
                        profile = get_user_profile(user.id)
                        if profile:
                            st.session_state.username = profile.get('username', user.email)
                            st.session_state.role = profile.get('role', 'user')
                        else:
                            st.session_state.username = user.email
                            st.session_state.role = 'user'
                        
                        st.success(f"Bienvenue {st.session_state.username} ✅")
                        st.rerun()
                    else:
                        st.error("Email ou mot de passe incorrect ❌")
                else:
                    st.error("Veuillez remplir tous les champs")
    
    with tab2:
        st.subheader("Créer un compte")
        with st.form("signup_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Nouveau mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            bouton = st.form_submit_button("Créer un compte")
            
            if bouton:
                if new_email and new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if ajout_user(new_email, new_password):
                                st.success("Compte créé avec succès ! ✅")
                                st.info("Vérifiez votre email pour confirmer votre inscription, puis connectez-vous.")
                            else:
                                st.error("Erreur lors de la création du compte ❌")
                        else:
                            st.error("Le mot de passe doit contenir au moins 6 caractères")
                    else:
                        st.error("Les mots de passe ne correspondent pas ❌")
                else:
                    st.error("Veuillez remplir tous les champs")

def logout():
    """Déconnexion"""
    try:
        supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.email = None
        st.session_state.username = None
        st.session_state.role = None
        st.success("Déconnexion réussie!")
    except Exception as e:
        st.error(f"Erreur lors de la déconnexion: {str(e)}")

def is_authenticated():
    """Vérifier si l'utilisateur est connecté"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Récupérer l'utilisateur actuel"""
    if is_authenticated():
        return {
            'user_id': st.session_state.get('user_id'),
            'email': st.session_state.get('email'),
            'username': st.session_state.get('username'),
            'role': st.session_state.get('role', 'user')
        }
    return None

def check_auth_session():
    """Vérifier s'il y a une session active"""
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state.authenticated = True
            st.session_state.user_id = session.user.id
            st.session_state.email = session.user.email
            
            # Récupérer le profil
            profile = get_user_profile(session.user.id)
            if profile:
                st.session_state.username = profile.get('username', session.user.email)
                st.session_state.role = profile.get('role', 'user')
            else:
                st.session_state.username = session.user.email
                st.session_state.role = 'user'
            
            return True
    except:
        pass
    return False

# Fonctions pour la compatibilité avec votre code existant
def afficher():
    """Afficher tous les utilisateurs (pour les admins)"""
    try:
        if get_current_user() and get_current_user()['role'] == 'admin':
            response = supabase.table("profile").select("*").execute()
            return response.data if response.data else []
        else:
            st.warning("Accès non autorisé")
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération: {str(e)}")
        return []