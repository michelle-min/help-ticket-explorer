import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import datetime

# Page title
st.set_page_config(page_title='Ticket Data Explorer', page_icon='📊')
st.title('📊 Support Ticket Data Explorer')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select ticket asignee(s) in the drop-down selection box and then 2. Select the date duration from the slider widget. This will generate an updated editable DataFrame and line plot.')
  
st.subheader('How many support tickets were resolved?')

# Load data
df = pd.read_csv('data/halp_tickets.csv', parse_dates=True)
df.created = pd.to_datetime(df.created)
df.closed = pd.to_datetime(df.closed)
df.first_response = pd.to_timedelta(df.first_response)
df.deadline = pd.to_datetime(df.deadline)
df['year'] = df.created.dt.year

# Input widgets
## Assignee selection
assignee_list = df.assignee.unique()
assignee_selection = st.multiselect('Select assignee', assignee_list, ['Chun Ying Wang','Michelle Min','Dominique Janvier','Aaron Buchanan','Julia Wood','Hassan Chaudhry'])

## Date selection
date_range = (datetime.datetime(2021,1,27), datetime.datetime(2024,3,1))
preselected_dates = (datetime.datetime(2022,9,1), datetime.datetime(2024,3,1))

selected_min, selected_max = st.slider(
    "Select date range",
    value=preselected_dates,
    min_value=date_range[0],
    max_value=date_range[1],
    step=datetime.timedelta(days=1),
    format="YYYY-MM-DD"
)

st.divider()

## Create DataFrame
df_selection = df[df.assignee.isin(assignee_selection) & (df.created >= selected_min) & (df.created <= selected_max)]
df_average_time = df_selection.pivot_table(index='year', columns='assignee', values='first_response')
df_count_num = df_selection.pivot_table(index='year', columns='assignee', values='id', aggfunc='count', fill_value=0)

# Display DataFrame of Response Time
st.caption("Average Time to First Response")

df_editor = st.data_editor(df_average_time, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("year")},
                            num_rows="dynamic")

# Display chart
st.caption("Number of Assigned Tickets")
df_chart = pd.melt(df_count_num.reset_index(), id_vars='year', var_name='assignee', value_name='id')

chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('id:Q', title='Count'),
            color='assignee:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)