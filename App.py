import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def get_data():
    df = pd.read_csv('data/COVID-19-geographic-disbtribution-worldwide.xlsx', keep_default_na=False, na_values='', engine="openpyxl")
    df_geo = df.dropna(subset=['geoId']).pivot(index='dateRep', columns='geoId', values=['cases', 'deaths'])
    return df_geo

try:
    df = get_data()
    countries = st.multiselect(
        "Choose countries", list(df.columns)
    )

    if not countries:
        st.error("Please select at least one country.")
    """
    else:

        data =
        st.write("### Data Visualisation")

        chart = 

        st.altair_chart(chart, use_container_width=True)
    """