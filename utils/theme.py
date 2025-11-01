import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import streamlit as st 
import  plotly.graph_objects as go
# definition des themes
themes={
    "light":{
        "primary" :"#000000",
        "secondary":"#F5F5F5",
         "text" :"#000000",
         "select" :"#0000005E",
         "plotly":"plotly_white",},
     "dark":{
        "primary" :"#ffffff",
        "secondary":"#1E1E1E4E",
         "text" :"#FFFFFF",
         "select" :"#3D4F8A92",
         "plotly":"plotly_dark",
    }
}
def init_theme(default_theme='light') :
    # initialiser le theme dans la session
    if 'theme' not in st.session_state :
        st.session_state['theme']=default_theme
def toggle_theme() :
    # basculer entre le mode clair et sombre
    st.session_state.theme=("dark" if st.session_state.theme=='light'else "light")
    st.rerun()
def current_theme() :
       #init_theme()
       # utilisation du  theme courant sur le graphique
       return  themes[st.session_state.theme]        
def plotly_templete() :
     # appliquer le theme sur le graphique
     theme=current_theme()
     return go.layout.Template(layout=dict(
          paper_bgcolor=theme["primary"], # font general,
          plot_bgcolor=theme["secondary"],# font graphique,
          font=dict(color=theme["text"])#couleur texte
     ))
def get_color() :
        theme =current_theme()
        return  {"container":{"background-color":theme['secondary']},"nav-link":{"background-color":theme['select']}}

def laod_css() :
     # appliquer du css 
     with open("assets\custom.css") as f :
              st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True) 
     
def apply_theme() :
    # application du theme sur l app
    theme=current_theme()
    st.markdown(f"""<style>
                .body {{
                        background-color:{theme['primary']};
                        color :{theme['text']};}}
                 .stApp{{
                        background-color:{theme['secondary']}!important;
                        color :{theme['text']};
    }}[data-testid="stSidebar"] {{background-color:{theme['secondary']}!important;color:{theme['text']}!important;}}
    .stSelectbox label,.stMultiSelect label {{background-color:{theme['select']};color :{theme['text']}}}
    .stSelectbox,.stMultiSelect{{background-color:{theme['secondary']};color :{theme['text']}}}
    div[data-testid="stMetric"]{{background-color:{theme['select']}}}
    div[data-testid="stMetricLabel"]>div:nth-child(1){{color:{theme['text']}}}</style>""",unsafe_allow_html=True)
   
   
   
