import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import json
import shap
import joblib as job
import matplotlib.pyplot as plt
import tempfile 
import os
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric
from evidently.metric_preset import DataDriftPreset 
@st.cache_resource
def recuperation(url: str) -> str:
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        # Pourquoi : mode="wb" évite les problèmes d’écriture binaire. timeout et message détaillé facilitent le debug.
        # ouvrir le tempfile en binaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".joblib", mode="wb") as tmp_file:
            tmp_file.write(r.content)
            return tmp_file.name
    except requests.RequestException as e:
        st.error(f"Impossible de se connecter à l'API Flask pour récupérer le model. Erreur : {e}")
        st.stop()
def drift():
    base = os.path.join(os.getcwd(), "dataset")  # si tu utilises volume, c'est /app/dataset
    path_old = os.path.join(base, "test.csv") 
    path_new = os.path.join(base, "train.csv")
    if not os.path.exists(path_old) or not os.path.exists(path_new):
        st.error(f"Fichiers drift introuvables: {path_old} ou {path_new}")
        st.stop()
    data_ancien = pd.read_csv(path_old)
    data_nouveau = pd.read_csv(path_new)
    return data_ancien, data_nouveau
                    
@st.cache_data
def dataframe(row_dict):
    col_pay = [f"PAY_{i}" for i in range(1, 7)]
    col_amt = [f"PAY_AMT{i}" for i in range(1, 7)]
    bill_col = [f"BILL_AMT{i}" for i in range(1, 7)]

    df = pd.DataFrame(row_dict, index=[0]) if isinstance(row_dict, dict) else pd.DataFrame(row_dict)
    # nettoyage minimal
    df["EDUCATION"] = df["EDUCATION"].replace([0, 5, 6], 4)
    df["SEX"] = df["SEX"].replace(['F', 'H'], [0, 1])
    df["MARRIAGE"] = df["MARRIAGE"].replace(0, 3)

    # calculs (vérifier que les colonnes existent)
    for c in col_amt + col_pay + bill_col:
        if c not in df.columns:
            df[c] = 0

    df["pay_mt_trend"] = df[col_amt].apply(lambda x: np.polyfit(range(1, 7), x, 1)[0], axis=1)
    df["AVG_pay"] = df[col_amt].mean(axis=1)
    df["retard"] = df[col_pay].apply(lambda x: (x > 0).sum(), axis=1)
    df["AVG_delai"] = df[col_pay].mean(axis=1)
    df["max_retard"] = df[col_pay].max(axis=1)
    df["total_pay_amt"] = df[col_amt].sum(axis=1)
    df["pay_to_credit"] = df["total_pay_amt"] / (df["LIMIT_BAL"] + 1)
    df["total_bill_amt"] = df[bill_col].sum(axis=1)
    df["total_bill_credit"] = df["total_bill_amt"] / (df["LIMIT_BAL"] + 1)
    df["avant"] = df[col_pay].apply(lambda x: (x <= 0).sum(), axis=1)

    for i in range(1, 7):
        df[f'PAY_{i}'] = df[f'PAY_{i}'].replace([4, 5, 6, 7, 8, 9], 4)

    return df

 
def explication_model(pipeline,dataset):
    try :
        model =pipeline.named_steps['xgbclassifier']
        feature=pipeline.named_steps['pipeline']['columntransformer']
        feature_name =feature.get_feature_names_out()
        seleckbest=pipeline.named_steps['pipeline']['selectkbest']
        mask =seleckbest.get_support()
        feature_reel=[col.split('__')[-1]for col in feature_name[mask]]
        names =[col.split('__')[-1]for col in feature_name]
        explainers=shap.Explainer(model)
        dataset_transform =seleckbest.transform(feature.transform(dataset))
        dataset_df= pd.DataFrame(dataset_transform,columns=feature_reel)
        shape_value=explainers(dataset_df)
        fig,ax =plt.subplots()
        ax=shap.plots.waterfall(shape_value[0])
        st.pyplot(fig)
    except Exception  as e :
           st.error(f"erreur lors  de l'explication shap :{e}")  
def run() :
    st.title("machine")
    bouton =st.sidebar.radio("menu",["prediction","log","drift"])
    if bouton == 'prediction' : 
        st.write("prediction")
        col1,col2,col3 =st.columns(3) 
        with st.form(key="12")  :
            with col1 :
                SEX =st.selectbox('selectionner le sex',["H","F"],key=1)
                EDUCATION=st.selectbox('education',[0,1,2,3,4,5,6],key=2)
                MARRIAGE =st.selectbox('etat civil',[0,1,2,3],key=3)
                AGE= st.number_input("age",value=30,key=4)
                LIMIT_BAL= st.number_input("montant limité",key=5)
                BILL_AMT1 =st.number_input("facture pour avril",key=6)
                BILL_AMT2 =st.number_input("facture pour mai",key=7)
                BILL_AMT3=st.number_input("facture pour juin",key=8)
            with col2 :
                PAY_1 =st.select_slider("situation d avril",[-2,-1,0,1,2,3],value=0,key=9)
                PAY_2 =st.select_slider("situation de mai",[-2,-1,0,1,2,3],value=0,key=10)
                PAY_3 =st.select_slider("situation de juin",[-2,-1,0,1,2,3],value=0,key=11)
                PAY_4 =st.select_slider("situation de juillet",[-2,-1,0,1,2,3],value=0,key=12)
                PAY_5 =st.select_slider("situation d aout",[-2,-1,0,1,2,3],value=0,key=13)
                PAY_6 =st.select_slider("situation de sept",[-2,-1,0,1,2,3],value=0,key=14)
                BILL_AMT6=st.number_input("facture pour sept",key=22)
            with col3 :
                BILL_AMT5=st.number_input("facture pour juillet",key=15)
                PAY_AMT1 =st.number_input("mt payé en avril",key=16)
                PAY_AMT2 =st.number_input("mt payé en mai",key=17)
                PAY_AMT3 =st.number_input("mt payé en juin",key=18)
                PAY_AMT4 =st.number_input("mt payé en juillet",key=19)
                PAY_AMT5 =st.number_input("mt payé en aout",key=23)
                PAY_AMT6 =st.number_input("mt payé en sept",key=24)
                BILL_AMT4=st.number_input("facture pour juillet",key=20)
                BILL_AMT5=st.number_input(" facture pour aout",key=21)
             
            dictionnaire ={"LIMIT_BAL":LIMIT_BAL,"SEX":SEX,"EDUCATION":EDUCATION,"MARRIAGE":MARRIAGE,"AGE":AGE,"PAY_1":PAY_1,"PAY_2":PAY_2
,"PAY_3":PAY_3,"PAY_4":PAY_4,"PAY_5":PAY_5,"PAY_6":PAY_6,"BILL_AMT1":BILL_AMT1,"BILL_AMT2":BILL_AMT2,"BILL_AMT3":BILL_AMT3,"BILL_AMT4":BILL_AMT4,"BILL_AMT5":BILL_AMT5,"BILL_AMT6":BILL_AMT6,
"PAY_AMT1":PAY_AMT1,"PAY_AMT2":PAY_AMT2,"PAY_AMT3":PAY_AMT3,"PAY_AMT4":PAY_AMT4,"PAY_AMT5":PAY_AMT5,"PAY_AMT6":PAY_AMT6}      
            df=dataframe(dictionnaire)
            data=df.copy()
            df =df.squeeze() 
            sumit = st.form_submit_button()
            if sumit :
                with st.spinner('attend un peu') :
                  time.sleep(0.5)
                  try :
                    url = "http://flask-api:5000"
                    model_path=recuperation(f"{url}/model")
                    pipeline=job.load(model_path)
                    reponse=requests.post(f"{url}/predict",json=df.to_dict(),timeout=10)
                    try :  
                           reponse.raise_for_status()
                    except :
                         st.error(f"Erreur API /predict : status {reponse.status_code} - {reponse.text}")
                         st.stop()       
                    result=reponse.json()
                    if result['prediction']==0 :
                        st.write(f"le client ne va pas faire le defaut de paiement avec une probabilite de {result['probabilite']*100:.2f}%")
                        explication_model(pipeline,data)
                    else :
                         st.write(f" le client  va faire le defaut de paiement avec une probabilite de {result['probabilite']*100:.2f}%")
                         explication_model(pipeline,data)
                    #st.write(f"prediction :'defaut' if {result['prediction']} else 'pas de défaut'")
                  except Exception as e : 
                      st.error(f"Erreur inattendue côté Streamlit : {e}") 
                 
    elif bouton=="log"  :
        st.write("log")  
    else :
        st.write("drift")
        ancien ,nouveau=drift()
        # creer un rapport de datadrift
        report=Report(metrics=[DataDriftPreset(),DatasetDriftMetric()])
        # generer le rapport
        report.run(reference_data=ancien,current_data=nouveau)
        report_html=report.get_html()
        st.components.v1.html(report_html,height=900,scrolling=True)
         