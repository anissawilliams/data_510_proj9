import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

### PAGE SETUP  & LOAD DATA ###
st.set_page_config(layout="wide")

st.title("National Labor Statistics Dashboard")
df = pd.read_csv("nls97b.csv")
# Extract the number at the start and sort by it (handle NaNs)
df['degree_order'] = df['highestdegree'].str.extract(r'^(\d+)\.')[0]
df['degree_order'] = pd.to_numeric(df['degree_order'], errors='coerce')
df = df.sort_values('degree_order')

# Create ordered categorical (drop NaNs from categories)
valid_degrees = df['highestdegree'].dropna().unique()
df['highestdegree'] = pd.Categorical(
    df['highestdegree'],
    categories=valid_degrees,
    ordered=True
)

# Drop the temporary column
df = df.drop('degree_order', axis=1)

### SIDEBAR ###
st.sidebar.header("Select highest degree earned: ")
highest_degree = st.sidebar.multiselect("Select Degree Option", df['highestdegree'].unique())

if not highest_degree:
    df2 = df.copy()
else:
    df2 = df[df['highestdegree'].isin(highest_degree)].copy()
    # Keep only the selected categories in order
    df2['highestdegree'] = df2['highestdegree'].cat.remove_unused_categories()

### CHARTS ###
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bar Chart of Highest Degree v. Hours Slept")
    fig = px.bar(df2, x="highestdegree", y="nightlyhrssleep", template="seaborn", labels={'nightlyhrssleep': 'Hours Slept per Week', 'highestdegree': 'Highest Degree Earned'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Pie Chart of Highest Degree v. Gender")
    df_counts = df2.groupby("highestdegree")["gender"].count().reset_index()
    fig = px.pie(df_counts, names="highestdegree", values="gender", labels={"gender": "Count", "highestdegree": "Highest Degree Earned"})
    st.plotly_chart(fig, use_container_width=True)

# Time series in full width below
st.subheader("Time Series of Weeks Worked Per Year by Highest Degree")

# Create a list of the weeks worked columns
weeks_cols = [f'weeksworked{str(i).zfill(2)}' for i in range(0, 14)]

# Rename columns to reflect actual years
year_map = {f'weeksworked{str(i).zfill(2)}': 1996 + i for i in range(0, 14)}
df_renamed = df2.rename(columns=year_map)  # ✅ Use df2, not df!

# Reshape to long format
df_long = df_renamed.melt(id_vars='highestdegree',
                          value_vars=list(year_map.values()),
                          var_name='year',
                          value_name='weeksworked')

# ✅ CREATE THE time series CHART
# Group by year and degree, take the mean
df_agg = df_long.groupby(['year', 'highestdegree'])['weeksworked'].mean().reset_index()

fig = px.line(df_agg, x='year', y='weeksworked', color='highestdegree',
              markers=True, template="seaborn", labels={'weeksworked': 'Weeks Worked', 'year': 'Year'})
st.plotly_chart(fig, use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(df_agg.T.style.background_gradient(cmap="Blues"))
    csv = df_agg.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')