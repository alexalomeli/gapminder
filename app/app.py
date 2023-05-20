import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#Load data

population = pd.read_csv('population.csv')
life_expectancy = pd.read_csv('life_expectancy.csv')
gni_per_capita = pd.read_csv('gni_per_capita.csv')

#Matrix to table
population=population.melt(['country'], var_name= 'year', value_name='population')
gni_per_capita=gni_per_capita.melt(['country'], var_name= 'year', value_name='gni_per_capita')
life_expectancy=life_expectancy.melt(['country'], var_name= 'year', value_name='life_expectancy')

#Sort values before forward filling

population=population.sort_values(['country','year'], ascending=[True,False])
gni_per_capita=gni_per_capita.sort_values(['country','year'], ascending=[True,False])
life_expectancy=life_expectancy.sort_values(['country','year'], ascending=[True,False])

#Forward filling

population['population']=population['population'].ffill()
gni_per_capita['gni_per_capita']=gni_per_capita['gni_per_capita'].ffill()
life_expectancy['life_expectancy']=life_expectancy['life_expectancy'].ffill()

#Concatenate data

df=pd.merge(gni_per_capita, life_expectancy, on=['country','year'], how='inner')
df=pd.merge(df, population, on=['country','year'], how='inner')

#Replace k,M,B

def k_to_number(value):
    if 'k'in value:
        number=float(value.replace('k', ''))*1000
        return int(number)
    elif isinstance(value,float):
        return int(value)
    try:
        return int(value)
    except ValueError:
        return None
    
def M_to_number(value):
    if 'M'in value:
        number=float(value.replace('M', ''))*1000000
        return int(number)
    elif isinstance(value,float):
        return int(value)
    try:
        return int(value)
    except ValueError:
        return None
    
def B_to_number(value):
    if 'B'in value:
        number=float(value.replace('B', ''))*1000000000
        return int(number)
    elif isinstance(value,float):
        return int(value)
    try:
        return int(value)
    except ValueError:
        return None

df['population'] = [k_to_number(value) if isinstance(value, str) else value for value in df['population']]
df['gni_per_capita'] = [k_to_number(value) if isinstance(value, str) else value for value in df['gni_per_capita']]
df['life_expectancy'] = [k_to_number(value) if isinstance(value, str) else value for value in df['life_expectancy']]

df['population'] = [M_to_number(value) if isinstance(value, str) else value for value in df['population']]
df['gni_per_capita'] = [M_to_number(value) if isinstance(value, str) else value for value in df['gni_per_capita']]
df['life_expectancy'] = [M_to_number(value) if isinstance(value, str) else value for value in df['life_expectancy']]

df['population'] = [B_to_number(value) if isinstance(value, str) else value for value in df['population']]
df['gni_per_capita'] = [B_to_number(value) if isinstance(value, str) else value for value in df['gni_per_capita']]
df['life_expectancy'] = [B_to_number(value) if isinstance(value, str) else value for value in df['life_expectancy']]

# Drop rows with nan values in the 'population' column
df = df.dropna(subset=['population'])

st.title('Gapminder')

# Year slider
year = st.slider('Year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].max()))

# Country selection
countries = st.multiselect('Select Countries', df['country'].unique())

# Filter data based on year and selected countries
filtered_data = df[(df['year'] == year) & (df['country'].isin(countries))]

# Create bubble chart
fig = px.scatter(filtered_data, x='gni_per_capita', y='life_expectancy', size='population',
                 color='country', log_x=True, hover_data=['country'])

fig.update_layout(
    title='GNI per capita vs Life Expectancy',
    xaxis_title='Logarithmic GNI per capita',
    yaxis_title='Life Expectancy'
)

# Render the chart using Streamlit
st.plotly_chart(fig)