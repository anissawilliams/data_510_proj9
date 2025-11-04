import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px



### PAGE SETUP  & LOAD DATA ###
st.set_page_config(layout="wide")

st.title("National Labor Statistics Dashboard")
df = pd.read_csv("nls97b.csv")


### SIDEBAR ###
st.sidebar.header("Select highest degree earned: ")
highest_degree = st.sidebar.multiselect("Select Degree Option", df['highestdegree'].unique())

if not highest_degree:
     df2 = df.copy()
else:
    df2 = df[df['highestdegree'].isin(highest_degree)]



col1, col2 = st.columns(2)
with col1:
    st.subheader("Bar Chart of Highest Degree v. Hours Slept")
    fig = px.bar(df2, x="highestdegree", y="nightlyhrssleep", template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Pie Chart of Highest Degree v. Gender")

    df_counts = df2.groupby("highestdegree")["gender"].count().reset_index()
    fig = px.pie(df_counts, names="highestdegree", values="gender")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Time Series of Weeks Worked by Highest Degree")

    # Create a list of the weeks worked columns
    weeks_cols = [f'weeksworked{str(i).zfill(2)}' for i in range(0, 14)]

    # Rename columns to reflect actual years
    year_map = {f'weeksworked{str(i).zfill(2)}': 1996 + i for i in range(0, 14)}
    df_renamed = df.rename(columns=year_map)

    # Reshape to long format
    df_long = df_renamed.melt(id_vars='highestdegree',
                              value_vars=year_map.values(),
                              var_name='year',
                              value_name='weeksworked')


