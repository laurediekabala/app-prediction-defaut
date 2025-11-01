import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import streamlit as st 
from connection import auth_db as db
from streamlit_option_menu import option_menu
import home,analyse,machinelearning
from utils.theme import init_theme,toggle_theme,laod_css,apply_theme,get_color
st.set_page_config(page_title='app pro',layout='wide')
init_theme()
if st.button("changer theme") :
     toggle_theme()
     st.rerun()
     #apply_theme()
laod_css()
apply_theme()
#with open("assets/styles.css") as f :
      #st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True) 
#theme = st.sidebar.radio("🎨 Thème", ["Clair", "Sombre"])
#if "dark_mode" not in st.session_state :
     #st.session_state.dark_mode=False
#st.session_state.dark_mode=st.toggle("mode sombre",value=st.session_state.dark_mode)    
#if st.session_state.dark_mode:
    #st.markdown(
       # '''
        #<style>
        #.stApp {background-color: #0E1127; color: white; }
        # body {background-color: #0D1127; color: white; }
        #</style>
        #''',
        #unsafe_allow_html=True ) 
#else :
         #st.markdown(
        #'''
        #<style>
        #.stApp {background-color: #0D2127; color: white; } 
        #.st {background-color: #0D2127; color: white; }  
        #</style>
        #''',
        #unsafe_allow_html=True
    #)    
         
def app() :
    with st.sidebar :
        page =option_menu("Navigation",['accueil','analyse','machinelearning'],styles=get_color())
    if page=='accueil' :
            home.run()
    elif page=='analyse' :
            analyse.run()
    elif page=='machinelearning' :
            machinelearning.run()       
def apps() :
        with st.sidebar :
           page =option_menu("Navigation",['accueil','machinelearning'])
        if page=='accueil' :
            home.run()
        elif page=='machinelearning' :
            machinelearning.run()  
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    db.login()
    st.stop()   
# Accueil utilisateur
st.sidebar.markdown("---")
st.sidebar.write(f"👤 Connecté : {st.session_state.username}")
st.sidebar.write(f"🔐 Rôle : {st.session_state.role}")
if st.sidebar.button("🔓 Déconnexion"):
    st.session_state.authenticated = False
    st.experimental_rerun() 
# Navigation
if st.session_state.role == "admin":
     app()
else:
   apps()