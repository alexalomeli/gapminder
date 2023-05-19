import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Scatter plot
plt.scatter(filtered_data['gni_per_capita'], filtered_data['life_expectancy'], s=filtered_data['population'] / 1e6,
            c=filtered_data['country'], alpha=0.7, cmap='Set3')
plt.xlabel('GNI per capita')
plt.ylabel('Life Expectancy')
plt.title('Gapminder Visualization')
plt.colorbar(label='Country')
plt.xscale('log')
plt.xlim(100, 100000)
plt.ylim(30, 90)
plt.grid(True)

# Display the plot using Streamlit
st.pyplot(plt)

# Additional content
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

