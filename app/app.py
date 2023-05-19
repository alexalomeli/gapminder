import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    population = pd.read_csv('population.csv')
    life_expectancy = pd.read_csv('life_expectancy.csv')
    gni_per_capita = pd.read_csv('gni_per_capita.csv')

    # Forward fill missing values
    population = population.ffill()
    life_expectancy = life_expectancy.ffill()
    gni_per_capita = gni_per_capita.ffill()

    # Reshape data into tidy format
    population = population.melt(id_vars='country', var_name='year', value_name='population')
    life_expectancy = life_expectancy.melt(id_vars='country', var_name='year', value_name='life_expectancy')
    gni_per_capita = gni_per_capita.melt(id_vars='country', var_name='year', value_name='gni_per_capita')

    # Merge dataframes
    data = population.merge(life_expectancy, on=['country', 'year'])
    data = data.merge(gni_per_capita, on=['country', 'year'])

    return data

data = load_data()

st.title('Gapminder')

# Year slider
year = st.slider('Year', min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=int(data['year'].max()))

# Country selection
countries = st.multiselect('Select Countries', data['country'].unique())

# Filter data based on year and selected countries
filtered_data = data[(data['year'] == year) & (data['country'].isin(countries))]

fig = px.scatter(filtered_data, x='gni_per_capita', y='life_expectancy', size='population', color='country', log_x=True, hover_data=['country'])

fig.update_layout(
    title='GNI per capita vs Life Expectancy',
    xaxis_title='Logarithmic GNI per capita',
    yaxis_title='Life Expectancy'
)

st.plotly_chart(fig)
