import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import streamlit as st
import plotly.express as pl
from scipy.stats import chi2_contingency,kruskal,iqr
from appstreamlit.home import dataset
import numpy as np
from utils.theme import plotly_templete
#@st.cache_data
def table_bar(data,column,filtre) :
    data=data.loc[data['default payment next month'].isin(filtre)]
    data=data[column].value_counts().reset_index()
    return data
def run() :
    st.title("analyse")
    data,feature=dataset()
    with st.sidebar :
        st.subheader("filtrage")
        radio =st.radio('annalyse',["exploratoire","avancee"])
    if radio=='exploratoire' :
        filtre=st.multiselect('filtrage par defaut de paiement',[col for col in data['default payment next month'].unique()],default=[0,1])
        data=data.loc[data['default payment next month'].isin(filtre)]
        col1,col2= st.columns([2,2]) 
        with st.sidebar :
            objet_columns=[col for col in data.columns[1:4]]
            pay=[f"PAY_{i}"for i in range(1,7)]
            objet_columns.append('default payment next month')
            objet_columns=objet_columns+pay
            column_objet=st.selectbox("selectionner une variable categorielle",objet_columns)
            column_numeric=st.selectbox("selectionner une variable numerique",[col for col in data if col not in objet_columns])
            with col1 : 
                try :
                   tab=table_bar(data,column_objet,filtre)
                   if tab[column_objet].nunique()<=2:
                       fig=pl.pie(tab,names=tab.index,values='count',title=column_objet)
                       st.plotly_chart(fig,use_container_width=True,theme=None)
                   else : 
                       fig=pl.bar(tab,x=column_objet,y='count',color=column_objet,title=column_objet)
                       st.plotly_chart(fig)  
                except Exception  :
                    st.warning("veuillez selectionner une variable")
                with col2 :       
                        try :
                            fig = pl.histogram(data,x=column_numeric,title=column_numeric)
                            #fig.update_layout(template=plotly_templete())
                            st.plotly_chart(fig)  
                        except Exception  :
                            st.warning("veuillez selectionner une variable")   
        with st.container(height=270,border=True)  :
                col1,col2 =st.columns(2)
                with col1 :
                   with  st.container(height=180,border=True) :
                          objet_column= [col for col in data.columns[1:4]]+pay
                          col_obj1 =st.selectbox("select var cat1 ",objet_column,key=1)
                          col_obj2 =st.selectbox("select var cat2",objet_column,key=2)
                with col2 :
                   with  st.container(height=180,border=True) :
                          col_num1 =st.selectbox("select var num1",[col for col in data if col not in objet_columns],key=3)
                          col_num2 =st.selectbox("select var num2",[col for col in data if col not in objet_columns],key=4)          

                defaut =st.select_slider("defaut de paiement",[None,'default payment next month']) 
              
        col3,col4 =st.columns([2,1])
        with col3 :  
            if col_obj1!=col_obj2 :
                tab =data.groupby(col_obj1)[col_obj2].value_counts().reset_index() 
                fig =pl.bar(tab,x=col_obj2,y='count',color=col_obj1,title=f"rel entre {col_obj1} et {col_obj2}") 
                #fig.update_layout(template=plotly_templete())
                st.plotly_chart(fig) 
            else :
                 st.warning("veuillez insert 2 colonnes differentes",icon="🔥") 
        with col4 : 
               if col_num1!=col_num2 :
                fig =pl.scatter(data,x=col_num1,y=col_num2,title=f"rel entre {col_num1} et {col_num2}")
                #fig.update_layout(template=plotly_templete()) 
                st.plotly_chart(fig) 
               else :
                 st.warning("veuillez insert 2 colonnes differentes",icon="🔥")   
        col5,col6 =st.columns([2,2]) 
        with col5 :  
                tab =data.groupby("default payment next month")[col_obj1].value_counts().reset_index() 
                fig =pl.bar(tab,x=col_obj1,y='count',color='default payment next month',title=f"rel entre {col_obj1} et default payment next month") 
                #fig.update_layout(template=plotly_templete())
                st.plotly_chart(fig) 
        with col6 :  
                tab =data.groupby("default payment next month")[col_num1].value_counts().reset_index() 
                fig =pl.box(data,x="default payment next month",y=col_num1,color='default payment next month',title=f"rel entre {col_num1} et default payment next month") 
                #fig.update_layout(template=plotly_templete())
                st.plotly_chart(fig)                                       
        st.subheader("matrice de correlation")
        st.dataframe(data[[col for col in data if col not in objet_columns]].corr().style.background_gradient(cmap="Blues",high=0.2,low=0)) 
    else : 
        st.title("Analyse Avancée") 
        with st.container(height=120,border=True) :
            col1,col2,col3,col4 =st.columns(4)
            with col1 :
                filtrage_by_default=st.multiselect('select default',[col for col in feature["default payment next month"].unique()],default=feature["default payment next month"].unique())
            with col2 :
                    filtrage_by_sex=st.multiselect('select sex',[col for col in feature["SEX"].unique()],default=feature["SEX"].unique())
            with col3 :
                    filtrage_by_educat=st.multiselect('select education',[col for col in feature["EDUCATION"].unique()],default=feature["EDUCATION"].unique())
            with col4 :
                   filtrage_by_married=st.multiselect('select etat-civil',[col for col in feature["MARRIAGE"].unique()],default=feature["MARRIAGE"].unique())
        feature =feature.loc[(feature["default payment next month"].isin(filtrage_by_default))&(feature["SEX"].isin(filtrage_by_sex))&(feature["EDUCATION"].isin(filtrage_by_educat))&(feature["MARRIAGE"].isin(filtrage_by_married))] 
        with st.container(height=400,border=True) :
             col1,col2=st.columns(2) 
             with col1 :
                 st.metric('delai de paiement moyen',value=np.around(feature.AVG_delai.median(),2))  
                 st.metric('tendance de paiement median',value=np.around(feature.pay_mt_trend.median(),2))
                 st.metric('dispersion de tendance  paiement',value=np.around(iqr(feature.pay_mt_trend),2))
             with col2 :
                 #st.metric(':red[ratio pay et limit montant]',value=np.around(feature.pay_to_credit.mean(),2))  
                 #st.metric(':red[ratio de dispersion pay et limit montant ]',value=np.around(iqr(feature.pay_to_credit),2))
                 st.metric('ratio facture et limit montant',value=np.around(feature.total_bill_credit.median(),2))
                 st.metric('dispersion ratio facture et limit montant',value=np.around(iqr(feature.total_bill_credit),2))
        with st.expander("analyse") :
             columns=["SEX","MARRIAGE","EDUCATION","default payment next month","retard","non_retard","max_retard","AVG_delai"]
             retard=feature.retard.value_counts().reset_index() 
             fig=pl.bar(retard,x='retard',y='count',title="retard")
             #fig.update_layout(template=plotly_templete())
             st.plotly_chart(fig)  
             col1,col2 =st.columns(2)  
             with col1 :
                       var1 =st.selectbox("select la premiere var",[col for col in feature if col not in ["SEX","MARRIAGE","EDUCATION","default payment next month","retard","non_retard","max_retard","AVG_delai"]],key=1)
                       fig =pl.box(feature,x=var1,title=var1)
                       #fig.update_layout(template=plotly_templete())
                       st.plotly_chart(fig)
             with col2 :
                        var2 =st.selectbox("sele ct la premiere var",[col for col in feature if col not in ["SEX","MARRIAGE","EDUCATION","default payment next month","retard","non_retard","max_retard","AVG_delai"]],key=2) 
                        if var1==var2 : 
                             st.warning("veuillez deux colonnes differents",icon="🚨")    
                        else : 
                               fig =pl.scatter(feature,x=var1,title=f"{var1} et {var2}")
                               st.plotly_chart(fig)   
             st.dataframe(feature[[col for col in feature if col not in columns]].describe().style.background_gradient(cmap="Blues",high=0.2,low=0))
