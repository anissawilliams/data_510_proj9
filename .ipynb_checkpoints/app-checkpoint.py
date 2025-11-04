import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("National Labor Statistics Dashboard")
df = pd.read_csv("nls97b.csv")

st.set_page_config(layout="wide")
col1, col2 = st.columns(2) 

st.sidebar.header("Select highest degree earned: ")
highest_degree = st.sidebar.multiselect("Select Degree Option", df['highestdegree'].unique())

if not highest_degree:
    df2 = df.copy()
else:
    df2 = df['highestdegree'].isin(highest_degree)


print(df2.head())
with col1: 
    st.subheader("Bar Chart of Highest Degree v. Hours Slept")
    #fig = px.pie(df2, values="highestdegree", template="plotly_dark")
    #fig.update_traces(text='highestdegree', textposition="inside")
    #st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(df2, x="highestdegree", y="nightlyhrssleep", template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Pie Chart of Highest Degree v. Gender")
    #fig = px.pie(df2, values="highestdegree", template="plotly_dark")
    #fig.update_traces(text='highestdegree', textposition="inside")
    #st.plotly_chart(fig, use_container_width=True)

    df_counts = df2.groupby("highestdegree")["gender"].count().reset_index()
    fig = px.pie(df_counts, names="highestdegree", values="gender")
    st.plotly_chart(fig, use_container_width=True)







