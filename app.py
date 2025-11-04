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
    df2 = df['highestdegree'].isin(highest_degree)



    #filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
    #st.subheader('Time Series Analysis')

    #linechart = pd.DataFrame(
    #    filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    #fig2 = px.line(linechart, x="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000,
    #               template="gridon")
    #st.plotly_chart(fig2, use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    st.subheader("Bar Chart of Highest Degree v. Hours Slept")

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

    # Group by year and highest degree, then compute average weeks worked
    avg_weeks = df_long.groupby(['year', 'highestdegree'])['weeksworked'].mean().reset_index()
    fig = px.line(avg_weeks, x='year', y='weeksworked', labels={'weeksworked': 'Average Weeks Worked'}, color='highestdegree', height=500, width=1000, template="gridon")
    st.plotly_chart(fig)
