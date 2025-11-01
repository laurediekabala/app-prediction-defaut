import streamlit as st
from traitement import donnees
import pandas as pd
import plotly.express as pl
import numpy as pn
@st.cache_data
def dataset() :
      try :
        analyse=donnees.analyse()
        data=analyse.dataset(r'D:\application_default\dataset\default.xlsx')
        feature=analyse.feature_eng()
        column = ["pay_mt_trend","AVG_pay","retard","max_retard",'total_pay_amt','pay_to_credit',"total_bill_amt",'total_bill_credit','total_bill_credit',"non_retard","AVG_delai"]
        df= data.copy()[[col for col in data if col not in column]]     
        return df,feature 
      except Exception :
              st.warning("erreur  veuillez reouvrir l'application",icon="🚨")
def oultier(df) :
   columns =['SEX','MARRIAGE','EDUCATION','default payment next month','PAY_1','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']
   outliers_percent={}
   for col in df :
        if col not in columns :
                q1 =pn.percentile(df[col],25)
                q3 =pn.percentile(df[col],75)
                iqr=q3-q1
                inf=q1-1.5*iqr
                sup=q3+1.5*iqr
                outliers=df[(df[col]<inf)|(df[col]>sup)]
                percent=len(outliers)/len(df)*100
                outliers_percent[col]=round(percent,2)
   st.table(pd.Series(outliers_percent,name='% outliers'))     
def run() :
               data,feature=dataset()
              
               st.subheader("Bienvenu sur notre application",divider='rainbow')
               st.markdown('##')
               filtre=st.multiselect('filtrage par defaut de paiement',[col for col in data['default payment next month'].unique()])
               st.dataframe(data.loc[data['default payment next month'].isin(filtre)])
               st.header("Statistique")
               column=[col for col in data if col not in ["EDUCATION","MARRIAGE","SEX",'default payment next month']]
               st.dataframe(data.loc[data['default payment next month'].isin(filtre)][column].describe().style.background_gradient(cmap="Blues",high=0.2,low=0))
               st.write("les outliers")
               oultier(data)
               st.write(f"le dataset contient {data.loc[data['default payment next month'].isin(filtre)].shape[0]} lignes et {data.shape[1]} colonnes")