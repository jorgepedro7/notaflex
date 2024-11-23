import pandas as pd
import streamlit as st
# # Configurações padrão para o aplicativo
# default_aliquota_interna = 18.0  # Alíquota Interna padrão (%)
# default_aliquota_interestadual = 12.0  # Alíquota Interestadual padrão (%)

@st.cache_data
def load_icms_matrix():
    return pd.read_excel('.\origemdestino.xlsx', index_col=0)
icms_matrix = load_icms_matrix()

print(icms_matrix.head())