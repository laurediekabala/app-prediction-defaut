import streamlit as st
from traitement import donnees
import pandas as pd
import numpy as np
import os

@st.cache_data
def dataset():
    try:
        analyse_obj = donnees.analyse()
        path = os.path.join("appstreamlit", "dataset", "default.xlsx")
        data = analyse_obj.dataset(path)
        if data is None:
            st.warning("Le dataset n'a pas pu être chargé.", icon="🚨")
            return None
        feature = analyse_obj.feature_eng()
        
        # Supprimer certaines colonnes
        column_to_remove = [
            "pay_mt_trend", "AVG_pay", "retard", "max_retard",
            'total_pay_amt', 'pay_to_credit', "total_bill_amt",
            'total_bill_credit', "non_retard", "AVG_delai"
        ]
        df = data.copy()[[col for col in data if col not in column_to_remove]]
        return df, feature
    except Exception as e:
        st.warning(f"Erreur : {e}. Veuillez réouvrir l'application.", icon="🚨")
        return None

def oultier(df):
    columns = ['SEX','MARRIAGE','EDUCATION','default payment next month','PAY_1','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']
    outliers_percent = {}
    for col in df.columns:
        if col not in columns:
            q1 = np.percentile(df[col], 25)
            q3 = np.percentile(df[col], 75)
            iqr = q3 - q1
            inf = q1 - 1.5 * iqr
            sup = q3 + 1.5 * iqr
            outliers = df[(df[col] < inf) | (df[col] > sup)]
            percent = len(outliers) / len(df) * 100
            outliers_percent[col] = round(percent, 2)
    st.table(pd.Series(outliers_percent, name='% outliers'))

def run():
    result = dataset()
    if result is None:
        st.stop()  # Arrête l'exécution si dataset non chargé
    data, feature = result

    st.subheader("Bienvenue sur notre application")
    filtre = st.multiselect(
        'Filtrage par défaut de paiement',
        [col for col in data['default payment next month'].unique()]
    )
    if filtre:
        filtered_data = data[data['default payment next month'].isin(filtre)]
    else:
        filtered_data = data

    st.dataframe(filtered_data)

    st.header("Statistiques")
    columns_stat = [col for col in data.columns if col not in ["EDUCATION","MARRIAGE","SEX",'default payment next month']]
    st.dataframe(filtered_data[columns_stat].describe().style.background_gradient(cmap="Blues", high=0.2, low=0))

    st.write("Outliers par colonne")
    oultier(data)

    st.write(f"Le dataset contient {filtered_data.shape[0]} lignes et {data.shape[1]} colonnes")
