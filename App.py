import streamlit as st
import pandas as pd

@st.cache
def get_data():
    df = pd.read_excel('data/COVID-19-geographic-disbtribution-worldwide.xlsx', keep_default_na=False, na_values='', engine="openpyxl")
    df_geo = df.dropna(subset=['geoId']).pivot(index='dateRep', columns='geoId', values=['cases', 'deaths'])
    return df_geo

try:
    df = get_data()
    countries = st.multiselect(
        "Choose countries", list(df.columns)
    )



except:
    print("An exception occurred")
    st.markdown("This app don't work")