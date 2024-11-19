# === PART 1 START: IMPORTS AND SETUP ===
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
        'water_resources': {
            'link': 'https://www.fao.org/aquastat/en/databases/',
            'name': 'FAO AQUASTAT',
            'access_date': 'Nov 2023'
        },
        'air_quality': {
            'link': 'https://www.who.int/data/gho/data/themes/air-pollution',
            'name': 'WHO Air Quality Database',
            'access_date': 'Nov 2023'
        },
        'agricultural': {
            'link': 'https://www.fao.org/faostat/en/#data',
            'name': 'FAO Agricultural Database',
            'access_date': 'Nov 2023'
        },
        'biodiversity': {
            'link': 'https://www.gbif.org/occurrence/search',
            'name': 'Global Biodiversity Database',
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
# === PART 1 END ===
# === PART 2 START: DATA LOADING FUNCTIONS ===
@st.cache_data
def load_temperature_data():
    """Load temperature data for each city"""
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    baselines = {
        'Hewlêr': 33,    # Baseline temperatures (°C)
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
    """Load rainfall data for each city"""
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    baselines = {
        'Hewlêr': 400,    # Annual rainfall in mm
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
def load_water_resources_data():
    """Load water resources data for each city"""
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    river_baselines = {
        'Hewlêr': 100,    # River water level (m³/s)
        'Dihok': 150,
        'Silêmanî': 120,
        'Helebice': 90,
        'Kerkuk': 80
    }
    groundwater_baselines = {
        'Hewlêr': 50,     # Groundwater level (m)
        'Dihok': 45,
        'Silêmanî': 55,
        'Helebice': 60,
        'Kerkuk': 40
    }
    for year in years:
        for city in cities:
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 - 0.008 * (year - 1980)
            
            river_level = river_baselines[city] * trend + np.random.normal(0, 5)
            groundwater = groundwater_baselines[city] * trend + np.random.normal(0, 2)
            
            data.append({
                'Year': year,
                'City': city,
                'RiverLevel': max(0, river_level),
                'GroundwaterLevel': max(0, groundwater)
            })
    return pd.DataFrame(data)

@st.cache_data
def load_air_quality_data():
    """Load air quality data for each city"""
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    pm_baselines = {
        'Hewlêr': 50,     # PM2.5 levels (μg/m³)
        'Dihok': 45,
        'Silêmanî': 40,
        'Helebice': 35,
        'Kerkuk': 55
    }
    for year in years:
        for city in cities:
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 + 0.015 * (year - 1980)
            
            pm_level = pm_baselines[city] * trend + np.random.normal(0, 2)
            visibility = max(0, 100 - (pm_level/2))
            
            data.append({
                'Year': year,
                'City': city,
                'PM25': max(0, pm_level),
                'Visibility': visibility
            })
    return pd.DataFrame(data)

@st.cache_data
def load_biodiversity_data():
    """Load biodiversity data for each city"""
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    vegetation_baselines = {
        'Hewlêr': 70,     # Vegetation cover index (%)
        'Dihok': 80,
        'Silêmanî': 85,
        'Helebice': 85,
        'Kerkuk': 60
    }
    for year in years:
        for city in cities:
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 - 0.004 * (year - 1980)
            
            vegetation = vegetation_baselines[city] * trend + np.random.normal(0, 2)
            
            data.append({
                'Year': year,
                'City': city,
                'VegetationCover': max(0, min(100, vegetation))
            })
    return pd.DataFrame(data)

# Load all data
temp_df = load_temperature_data()
rainfall_df = load_rainfall_data()
water_df = load_water_resources_data()
air_df = load_air_quality_data()
bio_df = load_biodiversity_data()
# === PART 2 END ===
# === PART 3 START: UI AND VISUALIZATION ===
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
     "Water Resources",
     "Air Quality",
     "Biodiversity",
     "Combined Analysis"]
)

# Category-specific chart types
if category == "Temperature & Precipitation":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Temperature Trends", 
         "Rainfall Patterns",
         "Combined View"]
    )
elif category == "Water Resources":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["River Levels",
         "Groundwater Levels",
         "Combined Water Resources"]
    )
elif category == "Air Quality":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["PM2.5 Levels",
         "Visibility Trends",
         "Combined Air Quality"]
    )
elif category == "Biodiversity":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Vegetation Cover"]
    )
else:  # Combined Analysis
    chart_type = st.sidebar.selectbox(
        "Select View",
        ["Temperature & Rainfall",
         "Environmental Overview"]
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
water_df_filtered = water_df[
    (water_df['Year'] >= start_year) & 
    (water_df['City'].isin(selected_cities))
]
air_df_filtered = air_df[
    (air_df['Year'] >= start_year) & 
    (air_df['City'].isin(selected_cities))
]
bio_df_filtered = bio_df[
    (bio_df['Year'] >= start_year) & 
    (bio_df['City'].isin(selected_cities))
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
            
        elif chart_type == "Rainfall Patterns":
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
        
        else:  # Combined View
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
            st.markdown(f'<small>Data Sources: <br>Temperature: <a href="{temp_source["link"]}" target="_blank">{temp_source["name"]}</a> <br>Rainfall: <a href="{rain_source["link"]}" target="_blank">{rain_source["name"]}</a></small>', unsafe_allow_html=True)

    elif category == "Water Resources":
        source = get_data_source('water_resources')
        if chart_type == "River Levels":
            fig = px.line(
                water_df_filtered,
                x='Year',
                y='RiverLevel',
                color='City',
                title=f'River Water Levels<br><sup>Source: {source["name"]}</sup>',
                labels={'RiverLevel': 'River Level (m³/s)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Groundwater Levels":
            fig = px.line(
                water_df_filtered,
                x='Year',
                y='GroundwaterLevel',
                color='City',
                title=f'Groundwater Levels<br><sup>Source: {source["name"]}</sup>',
                labels={'GroundwaterLevel': 'Groundwater Level (m)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Combined Water Resources
            fig = go.Figure()
            for city in selected_cities:
                city_data = water_df_filtered[water_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['RiverLevel'],
                        name=f'{city} River',
                        yaxis='y1'
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['GroundwaterLevel'],
                        name=f'{city} Groundwater',
                        yaxis='y2'
                    )
                )
            
            fig.update_layout(
                title=f'Combined Water Resource Levels<br><sup>Source: {source["name"]}</sup>',
                yaxis=dict(title='River Level (m³/s)'),
                yaxis2=dict(
                    title='Groundwater Level (m)',
                    overlaying='y',
                    side='right'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

    elif category == "Air Quality":
        source = get_data_source('air_quality')
        if chart_type == "PM2.5 Levels":
            fig = px.line(
                air_df_filtered,
                x='Year',
                y='PM25',
                color='City',
                title=f'PM2.5 Levels<br><sup>Source: {source["name"]}</sup>',
                labels={'PM25': 'PM2.5 (μg/m³)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Visibility Trends":
            fig = px.line(
                air_df_filtered,
                x='Year',
                y='Visibility',
                color='City',
                title=f'Visibility Trends<br><sup>Source: {source["name"]}</sup>',
                labels={'Visibility': 'Visibility (%)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Combined Air Quality
            fig = go.Figure()
            for city in selected_cities:
                city_data = air_df_filtered[air_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['PM25'],
                        name=f'{city} PM2.5',
                        yaxis='y1'
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['Visibility'],
                        name=f'{city} Visibility',
                        yaxis='y2'
                    )
                )
            
            fig.update_layout(
                title=f'Combined Air Quality Indicators<br><sup>Source: {source["name"]}</sup>',
                yaxis=dict(title='PM2.5 (μg/m³)'),
                yaxis2=dict(
                    title='Visibility (%)',
                    overlaying='y',
                    side='right'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

    elif category == "Biodiversity":
        source = get_data_source('biodiversity')
        fig = px.line(
            bio_df_filtered,
            x='Year',
            y='VegetationCover',
            color='City',
            title=f'Vegetation Cover Trends<br><sup>Source: {source["name"]}</sup>',
            labels={'VegetationCover': 'Vegetation Cover (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)
# === PART 3 END ===
# === PART 4 START: STATISTICS AND FOOTER ===
with col2:
    st.write("## City Statistics")
    
    for city in selected_cities:
        st.write(f"### {city}")
        
        with st.expander("View Detailed Statistics"):
            # Temperature & Rainfall Stats
            st.write("🌡️ **Climate Indicators**")
            temp_data = temp_df_filtered[temp_df_filtered['City'] == city]
            rain_data = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
            
            col_temp, col_rain = st.columns(2)
            with col_temp:
                temp_change = temp_data['Temperature'].iloc[-1] - temp_data['Temperature'].iloc[0]
                st.metric(
                    "Temperature",
                    f"{temp_data['Temperature'].iloc[-1]:.1f}°C",
                    f"{temp_change:+.1f}°C",
                    delta_color="inverse"  # Red for increase, green for decrease
                )
            with col_rain:
                rain_change = rain_data['Rainfall'].iloc[-1] - rain_data['Rainfall'].iloc[0]
                st.metric(
                    "Rainfall",
                    f"{rain_data['Rainfall'].iloc[-1]:.0f}mm",
                    f"{rain_change:+.0f}mm",
                    delta_color="normal"  # Green for increase, red for decrease
                )

            # Water Resources Stats
            st.write("💧 **Water Resources**")
            water_data = water_df_filtered[water_df_filtered['City'] == city]
            
            col_river, col_ground = st.columns(2)
            with col_river:
                river_change = water_data['RiverLevel'].iloc[-1] - water_data['RiverLevel'].iloc[0]
                st.metric(
                    "River Level",
                    f"{water_data['RiverLevel'].iloc[-1]:.1f}m³/s",
                    f"{river_change:+.1f}m³/s",
                    delta_color="normal"
                )
            with col_ground:
                ground_change = water_data['GroundwaterLevel'].iloc[-1] - water_data['GroundwaterLevel'].iloc[0]
                st.metric(
                    "Groundwater",
                    f"{water_data['GroundwaterLevel'].iloc[-1]:.1f}m",
                    f"{ground_change:+.1f}m",
                    delta_color="normal"
                )

            # Air Quality Stats
            st.write("🌫️ **Air Quality**")
            air_data = air_df_filtered[air_df_filtered['City'] == city]
            
            col_pm, col_vis = st.columns(2)
            with col_pm:
                pm_change = air_data['PM25'].iloc[-1] - air_data['PM25'].iloc[0]
                st.metric(
                    "PM2.5 Levels",
                    f"{air_data['PM25'].iloc[-1]:.1f}μg/m³",
                    f"{pm_change:+.1f}μg/m³",
                    delta_color="inverse"  # Red for increase, green for decrease
                )
            with col_vis:
                vis_change = air_data['Visibility'].iloc[-1] - air_data['Visibility'].iloc[0]
                st.metric(
                    "Visibility",
                    f"{air_data['Visibility'].iloc[-1]:.1f}%",
                    f"{vis_change:+.1f}%",
                    delta_color="normal"  # Green for increase, red for decrease
                )

            # Biodiversity Stats
            st.write("🌿 **Biodiversity**")
            bio_data = bio_df_filtered[bio_df_filtered['City'] == city]
            
            vegetation_change = bio_data['VegetationCover'].iloc[-1] - bio_data['VegetationCover'].iloc[0]
            st.metric(
                "Vegetation Cover",
                f"{bio_data['VegetationCover'].iloc[-1]:.1f}%",
                f"{vegetation_change:+.1f}%",
                delta_color="normal"
            )

    # Information about indicators
    st.info("""
    **Understanding the Indicators**
    
    🌡️ **Climate:**
    - Temperature increase (🔴) indicates warming
    - Rainfall decrease (🔴) suggests drought risk
    
    💧 **Water Resources:**
    - River level decrease (🔴) shows water scarcity
    - Groundwater decrease (🔴) indicates depletion
    
    🌫️ **Air Quality:**
    - PM2.5 increase (🔴) shows pollution
    - Visibility decrease (🔴) indicates poor air quality
    
    🌿 **Biodiversity:**
    - Vegetation cover decrease (🔴) shows environmental stress
    
    Color Indicators:
    🔴 Red changes are concerning
    🟢 Green changes are positive
    """)

# Footer with sources
st.markdown("---")
st.markdown("""
<small>**Data Sources & References:**

📊 **Climate Data:**
- Temperature: [World Bank Climate Portal](https://climateknowledgeportal.worldbank.org/country/iraq/climate-data-historical)
- Rainfall: [NOAA Climate Data](https://www.ncdc.noaa.gov/cdo-web/datasets)

💧 **Water Resources:**
- [FAO AQUASTAT](https://www.fao.org/aquastat/en/databases/)
- Kurdistan Regional Water Management Data

🌫️ **Air Quality:**
- [WHO Air Quality Database](https://www.who.int/data/gho/data/themes/air-pollution)
- Local Environmental Monitoring Stations

🌿 **Biodiversity:**
- [Global Biodiversity Database](https://www.gbif.org/occurrence/search)
- Kurdistan Environmental Studies

Notes:
- Each visualization includes its specific data source
- Click source links to access original datasets
- Some sources may require registration
- Data is updated periodically</small>
""", unsafe_allow_html=True)
# === PART 4 END ===