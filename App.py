import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from streamLitFunc import streamLitFunc
from bokeh.plotting import figure



def get_data():
    df = pd.read_excel('data/COVID-19-geographic-disbtribution-worldwide.xlsx', keep_default_na=False, na_values='', engine="openpyxl")
    df_geo = df.dropna(subset=['geoId']).pivot(index='dateRep', columns='geoId', values=['cases', 'deaths'])
    return df_geo


df = get_data()
countries = st.multiselect(
    "Choose countries", list(df["cases"].columns)
)

# First plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(df.index, df["cases"][countries])

ax.set_title("Number of cases by date")

ax.set_xlabel("Date")
ax.set_ylabel("Number of cases")

ax.legend(countries)

st.write(fig)

# Second plot
date = "20200101"

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(df['cases'][countries].rolling(14, win_type='triang').mean().loc[date:])

ax.set_title("Number of cases by date")

ax.set_xlabel("Date")
ax.set_ylabel("Number of cases")

ax.legend(countries)

st.write(fig)

# Third plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(np.log(df['cases'][countries].rolling(14, win_type='triang').mean().loc[date:]))

ax.set_title("Number of cases by date")

ax.set_xlabel("Date")
ax.set_ylabel("Number of cases")

ax.legend(countries)

st.write(fig)

# Fourth plot
date_end = "20200501"

df['daynum'] = (df.index - df.index.min()).days
measure  = 'cases'
pmeasure = 'pcases'

if type(date_end)  != str:
    date_end = str(date_end)


df_pred = pd.DataFrame({'x':df['daynum'], 'y':df[measure][countries].loc[:date_end].rolling(7).mean()})
deg = 4

df_pred = df_pred[df_pred['y'] > 100]
fit = np.polyfit(x=df_pred['x'], y=df_pred['y'], deg=deg, full=True)
df_pred['p'] = np.polyval(fit[0], df_pred['x'])
df[(pmeasure, countries)] = 10 ** np.polyval(fit[0], df['daynum'])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(df[[(measure, countries), (pmeasure, countries)]])

ax.set_title("Number of cases by date")

ax.set_xlabel("Date")
ax.set_ylabel("Number of cases")

ax.legend(countries)

st.write(fig)
