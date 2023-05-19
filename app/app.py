import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def k_to_number(value):
    if isinstance(value, str):
        if 'k' in value:
            number = float(value.replace('k', '')) * 1000
            return int(number)
    return value

def M_to_number(value):
    if isinstance(value, str):
        if 'M' in value:
            number = float(value.replace('M', '')) * 1000000
            return int(number)
    return value

def B_to_number(value):
    if isinstance(value, str):
        if 'B' in value:
            number = float(value.replace('B', '')) * 1000000000
            return int(number)
    return value

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

df['population'] = df['population'].apply(lambda value: k_to_number(value) if isinstance(value, str) else value)
df['population'] = df['population'].apply(lambda value: M_to_number(value) if isinstance(value, str) else value)
df['population'] = df['population'].apply(lambda value: B_to_number(value) if isinstance(value, str) else value)

df['gni_per_capita'] = df['gni_per_capita'].apply(lambda value: k_to_number(value) if isinstance(value, str) else value)
df['gni_per_capita'] = df['gni_per_capita'].apply(lambda value: M_to_number(value) if isinstance(value, str) else value)
df['gni_per_capita'] = df['gni_per_capita'].apply(lambda value: B_to_number(value) if isinstance(value, str) else value)

df['life_expectancy'] = df['life_expectancy'].apply(lambda value: k_to_number(value) if isinstance(value, str) else value)
df['life_expectancy'] = df['life_expectancy'].apply(lambda value: M_to_number(value) if isinstance(value, str) else value)
df['life_expectancy'] = df['life_expectancy'].apply(lambda value: B_to_number(value) if isinstance(value, str) else value)

# Convert 'population' column to numeric values
df['population'] = pd.to_numeric(df['population'], errors='coerce')

# Calculate the maximum value for the size parameter
max_size = df['population'].max()

# Use the DataFrame for visualization
fig = px.scatter(df, x='gni_per_capita', y='life_expectancy', size='population',
                 hover_name='country', title='GNI per Capita vs Life Expectancy',
                 size_max=max_size)
fig.show()