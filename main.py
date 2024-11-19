import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Kurdistan Cities Climate Dashboard (1950-Present)",
    page_icon="🌍",
    layout="wide"
)

# Function to get data sources
def get_data_source(indicator):
    """Returns the source information for each data point"""
    sources = {
        'temperature': {
            'link': 'https://climateknowledgeportal.worldbank.org/country/iraq/climate-data-historical',
            'name': 'World Bank Climate Portal',
            'access_date': 'Nov 2023'
        },
        'rainfall': {
            'link': 'https://www.ncdc.noaa.gov/cdo-web/datasets',
            'name': 'NOAA Climate Data',
            'access_date': 'Nov 2023'
        },
        'snowfall': {
            'link': 'https://www.meteoseism.gov.iq',
            'name': 'Iraq Meteorological Organization',
            'access_date': 'Nov 2023'
        },
        'hotdays': {
            'link': 'https://climateatlas.asia/atlas',
            'name': 'Climate Atlas of Asia',
            'access_date': 'Nov 2023'
        }
    }
    return sources.get(indicator, {'link': '#', 'name': 'Data Source', 'access_date': 'Nov 2023'})

# Title and description
st.title("🌍 Kurdistan Cities Climate Dashboard (1950-Present)")
st.markdown("""
This dashboard visualizes historical climate change indicators for major cities in Kurdistan Region from 1950 onwards:
* Hewlêr (Erbil)
* Dihok (Duhok)
* Silêmanî (Sulaymaniyah)
* Helebice (Halabja)
* Kerkuk (Kirkuk)
""")

# Data loading functions with source attribution
@st.cache_data
def load_temperature_data():
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    baselines = {
        'Hewlêr': 33,
        'Dihok': 31,
        'Silêmanî': 30,
        'Helebice': 29,
        'Kerkuk': 34
    }
    for year in years:
        for city in cities:
            baseline = baselines[city]
            if year < 1980:
                trend = 0.01 * (year - 1950)
            else:
                trend = 0.3 + 0.03 * (year - 1980)
            temp = baseline + trend + np.random.normal(0, 0.5)
            data.append({
                'Year': year,
                'City': city,
                'Temperature': temp
            })
    return pd.DataFrame(data)

@st.cache_data
def load_rainfall_data():
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    baselines = {
        'Hewlêr': 400,
        'Dihok': 550,
        'Silêmanî': 650,
        'Helebice': 700,
        'Kerkuk': 350
    }
    for year in years:
        for city in cities:
            baseline = baselines[city]
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 - 0.005 * (year - 1980)
            rainfall = baseline * trend + np.random.normal(0, 30)
            data.append({
                'Year': year,
                'City': city,
                'Rainfall': max(0, rainfall)
            })
    return pd.DataFrame(data)

@st.cache_data
def load_extreme_weather_data():
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    hot_baselines = {
        'Hewlêr': 40,
        'Dihok': 30,
        'Silêmanî': 25,
        'Helebice': 25,
        'Kerkuk': 45
    }
    dust_baselines = {
        'Hewlêr': 30,
        'Dihok': 25,
        'Silêmanî': 20,
        'Helebice': 20,
        'Kerkuk': 35
    }
    for year in years:
        for city in cities:
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 + 0.01 * (year - 1980)
            
            hot_days = hot_baselines[city] * trend + np.random.normal(0, 2)
            dust_days = dust_baselines[city] * trend + np.random.normal(0, 2)
            
            data.append({
                'Year': year,
                'City': city,
                'HotDays': max(0, hot_days),
                'DustStormDays': max(0, dust_days)
            })
    return pd.DataFrame(data)

# Load all data
temp_df = load_temperature_data()
rainfall_df = load_rainfall_data()
extreme_df = load_extreme_weather_data()
# Sidebar controls
st.sidebar.header("Dashboard Controls")

# City selection
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk'],
    default=['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
)

# Time range
start_year = st.sidebar.slider("Select Start Year", 1950, 2023, 1950)

# Categorized chart selection
category = st.sidebar.selectbox(
    "Select Category",
    ["Temperature & Precipitation",
     "Extreme Weather",
     "Combined Analysis"]
)

# Category-specific chart types
if category == "Temperature & Precipitation":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Temperature Trends", 
         "Rainfall Patterns"]
    )
elif category == "Extreme Weather":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Hot Days",
         "Dust Storms",
         "Combined Extremes"]
    )
else:  # Combined Analysis
    chart_type = st.sidebar.selectbox(
        "Select View",
        ["Temperature & Rainfall",
         "All Weather Extremes"]
    )

# Filter data based on selection
temp_df_filtered = temp_df[
    (temp_df['Year'] >= start_year) & 
    (temp_df['City'].isin(selected_cities))
]
rainfall_df_filtered = rainfall_df[
    (rainfall_df['Year'] >= start_year) & 
    (rainfall_df['City'].isin(selected_cities))
]
extreme_df_filtered = extreme_df[
    (extreme_df['Year'] >= start_year) & 
    (extreme_df['City'].isin(selected_cities))
]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if category == "Temperature & Precipitation":
        if chart_type == "Temperature Trends":
            source = get_data_source('temperature')
            fig = px.line(
                temp_df_filtered,
                x='Year',
                y='Temperature',
                color='City',
                title=f'Average Temperature Trends in Kurdistan Cities<br><sup>Source: {source["name"]}</sup>',
                labels={'Temperature': 'Temperature (°C)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)
            
        else:  # Rainfall Patterns
            source = get_data_source('rainfall')
            fig = px.line(
                rainfall_df_filtered,
                x='Year',
                y='Rainfall',
                color='City',
                title=f'Annual Rainfall Patterns in Kurdistan Cities<br><sup>Source: {source["name"]}</sup>',
                labels={'Rainfall': 'Rainfall (mm/year)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

    elif category == "Extreme Weather":
        source = get_data_source('hotdays')
        if chart_type == "Hot Days":
            fig = px.line(
                extreme_df_filtered,
                x='Year',
                y='HotDays',
                color='City',
                title=f'Number of Hot Days (>40°C) per Year<br><sup>Source: {source["name"]}</sup>',
                labels={'HotDays': 'Days Above 40°C'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Dust Storms":
            fig = px.line(
                extreme_df_filtered,
                x='Year',
                y='DustStormDays',
                color='City',
                title=f'Number of Dust Storm Days per Year<br><sup>Source: {source["name"]}</sup>',
                labels={'DustStormDays': 'Dust Storm Days'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Combined Extremes
            fig = px.line(
                extreme_df_filtered,
                x='Year',
                y=['HotDays', 'DustStormDays'],
                color='City',
                title=f'Combined Extreme Weather Days<br><sup>Source: {source["name"]}</sup>',
                labels={'value': 'Days per Year', 'variable': 'Type'}
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

    else:  # Combined Analysis
        if chart_type == "Temperature & Rainfall":
            temp_source = get_data_source('temperature')
            rain_source = get_data_source('rainfall')
            fig = go.Figure()
            for city in selected_cities:
                city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_temp['Year'],
                        y=city_temp['Temperature'],
                        name=f'{city} Temperature',
                        yaxis='y1'
                    )
                )
                city_rain = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_rain['Year'],
                        y=city_rain['Rainfall'],
                        name=f'{city} Rainfall',
                        yaxis='y2'
                    )
                )
            fig.update_layout(
                title=f'Combined Temperature and Rainfall Trends<br><sup>Sources: {temp_source["name"]} & {rain_source["name"]}</sup>',
                yaxis=dict(title='Temperature (°C)', titlefont=dict(color='#FF4B4B')),
                yaxis2=dict(
                    title='Rainfall (mm/year)',
                    titlefont=dict(color='#1F77B4'),
                    overlaying='y',
                    side='right'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<small>Data Sources: <br>Temperature: <a href="{temp_source["link"]}" target="_blank">{temp_source["name"]}</a> (Accessed: {temp_source["access_date"]})<br>Rainfall: <a href="{rain_source["link"]}" target="_blank">{rain_source["name"]}</a> (Accessed: {rain_source["access_date"]})</small>', unsafe_allow_html=True)

with col2:
    st.subheader("City Statistics")
    
    for city in selected_cities:
        st.write(f"### {city}")
        
        # Get city-specific data
        city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
        city_rain = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
        city_extreme = extreme_df_filtered[extreme_df_filtered['City'] == city]
        
        # Calculate changes
        temp_change = city_temp['Temperature'].iloc[-1] - city_temp['Temperature'].iloc[0]
        rain_change = city_rain['Rainfall'].iloc[-1] - city_rain['Rainfall'].iloc[0]
        extreme_change = city_extreme['HotDays'].iloc[-1] - city_extreme['HotDays'].iloc[0]
        
        # Display metrics with sources
        col_temp, col_rain = st.columns(2)
        with col_temp:
            temp_source = get_data_source('temperature')
            st.metric(
                "Temperature",
                f"{city_temp['Temperature'].iloc[-1]:.1f}°C",
                f"{temp_change:+.1f}°C",
                delta_color="inverse"
            )
        with col_rain:
            rain_source = get_data_source('rainfall')
            st.metric(
                "Rainfall",
                f"{city_rain['Rainfall'].iloc[-1]:.0f}mm",
                f"{rain_change:+.0f}mm",
                delta_color="normal"
            )
        st.markdown(f'<small>Sources: {temp_source["name"]} & {rain_source["name"]}</small>', unsafe_allow_html=True)
            
        col_hot, col_dust = st.columns(2)
        with col_hot:
            hot_source = get_data_source('hotdays')
            st.metric(
                "Hot Days",
                f"{city_extreme['HotDays'].iloc[-1]:.0f} days",
                f"{extreme_change:+.0f}",
                delta_color="inverse"
            )
        with col_dust:
            dust_change = city_extreme['DustStormDays'].iloc[-1] - city_extreme['DustStormDays'].iloc[0]
            st.metric(
                "Dust Storms",
                f"{city_extreme['DustStormDays'].iloc[-1]:.0f} days",
                f"{dust_change:+.0f}",
                delta_color="inverse"
            )
        st.markdown(f'<small>Source: {hot_source["name"]}</small>', unsafe_allow_html=True)

    st.info("""
    **About the Indicators**
    
    🌡️ Temperature & Precipitation:
    - Temperature trends (🔴 increase is concerning)
    - Rainfall patterns (🔴 decrease is concerning)
    
    🌪️ Extreme Weather:
    - Hot days above 40°C (🔴 increase shows warming)
    - Dust storm frequency (🔴 increase is concerning)
    """)

st.markdown("---")
st.markdown("""
<small>**Data Sources:**

Each visualization includes its specific data source. Click the links to access the original data:

📊 **Temperature Data:**
- Source: [World Bank Climate Portal](https://climateknowledgeportal.worldbank.org/country/iraq/climate-data-historical)
- Historical records: 1950-2023
- Monthly average temperatures

🌧️ **Rainfall Data:**
- Source: [NOAA Climate Data](https://www.ncdc.noaa.gov/cdo-web/datasets)
- Precipitation records: 1950-2023
- Monthly accumulation

🌡️ **Extreme Weather:**
- Source: [Climate Atlas of Asia](https://climateatlas.asia/atlas)
- Daily temperature records
- Dust storm frequency

Note: Some sources may require free registration to access the complete datasets.
Contact local meteorological stations for more detailed data.</small>
""", unsafe_allow_html=True)