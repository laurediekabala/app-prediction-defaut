import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import streamlit as st 
from connection.auth import login, is_authenticated, get_current_user, logout, check_auth_session
from streamlit_option_menu import option_menu
import home, analyse, machinelearning
from utils.theme import init_theme, toggle_theme, laod_css, apply_theme, get_color

st.set_page_config(page_title='app pro', layout='wide')

# Initialisation du thème
init_theme()
if st.button("changer theme"):
    toggle_theme()
    st.rerun()

laod_css()
apply_theme()

def app():
    """Interface complète pour les admins"""
    with st.sidebar:
        page = option_menu("Navigation", ['accueil', 'analyse', 'machinelearning'], styles=get_color())
    
    if page == 'accueil':
        home.run()
    elif page == 'analyse':
        analyse.run()
    elif page == 'machinelearning':
        machinelearning.run()

def apps():
    """Interface limitée pour les utilisateurs normaux"""
    with st.sidebar:
        page = option_menu("Navigation", ['accueil', 'machinelearning'], styles=get_color())
    
    if page == 'accueil':
        home.run()
    elif page == 'machinelearning':
        machinelearning.run()

def main_app():
    """Application principale une fois connecté"""
    user = get_current_user()
    
    if not user:
        st.error("Erreur: Utilisateur non trouvé")
        logout()
        st.rerun()
        return
    
    # Sidebar avec informations utilisateur
    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 Connecté : {user['username']}")
    st.sidebar.write(f"📧 Email : {user['email']}")
    st.sidebar.write(f"🔐 Rôle : {user['role']}")
    
    if st.sidebar.button("🔓 Déconnexion"):
        logout()
        st.rerun()
    
    # Navigation basée sur le rôle
    if user['role'] == "user":
        app()
    else:
        apps()

def main():
    # Initialiser les variables de session si elles n'existent pas
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    # Vérifier s'il y a une session Supabase active
    if not st.session_state.get('authenticated'):
        check_auth_session()
    
    # Logique principale
    if is_authenticated():
        main_app()
    else:
        login()

# Point d'entrée principal
if __name__ == "__main__":
    main()