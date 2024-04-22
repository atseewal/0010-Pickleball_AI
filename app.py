"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

df

## Write a data frame

st.write("Here's our first attempt at using data to create a table:")
st.write(df)

## Styler objects

st.write("Styler object")
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20))
)

st.dataframe(dataframe.style.highlight_max(axis=0))

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20))
)

st.table(dataframe)

st.write("Draw a line chart")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data)

st.write("plot a map")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

st.write("Widgets")

x = st.slider('x')
st.write(x, 'squared is', x * x)

st.text_input("Your name", key="name")

st.session_state.name

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    
    chart_data


st.write("layout")

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile Phone")
)

add_slider = st.sidebar.slider(
    'select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
left_column.button("Press me!")

with right_column:
    chosen = st.radio(
        'sorting hat',
        ("Gryffindor", "Ravenclaw",)
    )
    st.write(f'you are in {chosen} house!')

'starting a long computation...'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Itration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'...and now we\'re done!'