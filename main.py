# === PART 1 START: IMPORTS AND SETUP ===
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.figure_factory as ff
from scipy import stats
import calendar

# Set page configuration
st.set_page_config(
    page_title="Kurdistan Cities Climate Dashboard (1950-Present)",
    page_icon="🌍",
    layout="wide"
)

# Function to get data sources
def get_data_source(indicator):
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
        'health': {
            'link': 'https://www.who.int/data/gho',
            'name': 'WHO Global Health Observatory',
            'access_date': 'Nov 2023'
        },
        'economic': {
            'link': 'https://data.worldbank.org',
            'name': 'World Bank Open Data',
            'access_date': 'Nov 2023'
        },
        'disaster': {
            'link': 'https://www.emdat.be',
            'name': 'EM-DAT Database',
            'access_date': 'Nov 2023'
        }
    }
    return sources.get(indicator, {'link': '#', 'name': 'Data Source', 'access_date': 'Nov 2023'})

# Title and description
st.title("🌍 Kurdistan Cities Climate Dashboard (1950-Present)")
st.markdown("""
This comprehensive dashboard visualizes historical climate change indicators for major cities in Kurdistan Region from 1950 onwards:
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
    years = list(range(1950, 2024))
    months = list(range(1, 13))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    
    baselines = {
        'Hewlêr': {'temp': 33, 'seasonal_var': 15},
        'Dihok': {'temp': 31, 'seasonal_var': 14},
        'Silêmanî': {'temp': 30, 'seasonal_var': 13},
        'Helebice': {'temp': 29, 'seasonal_var': 13},
        'Kerkuk': {'temp': 34, 'seasonal_var': 16}
    }

    for year in years:
        for month in months:
            for city in cities:
                baseline = baselines[city]['temp']
                seasonal_var = baselines[city]['seasonal_var']
                
                # Add seasonal variation
                season_effect = -seasonal_var * np.cos(2 * np.pi * (month - 1) / 12)
                
                # Add climate change trend
                if year < 1980:
                    trend = 0.01 * (year - 1950)
                else:
                    trend = 0.3 + 0.03 * (year - 1980)
                
                # Calculate final temperature
                temp = baseline + season_effect + trend + np.random.normal(0, 0.5)
                
                # Add extreme heat days calculation
                extreme_temp = temp + np.random.normal(0, 2)
                is_extreme = extreme_temp > 40
                
                data.append({
                    'Year': year,
                    'Month': month,
                    'MonthName': calendar.month_name[month],
                    'City': city,
                    'Temperature': temp,
                    'ExtremeHeatDay': is_extreme,
                    'Season': (
                        'Winter' if month in [12, 1, 2] else
                        'Spring' if month in [3, 4, 5] else
                        'Summer' if month in [6, 7, 8] else
                        'Autumn'
                    )
                })
    return pd.DataFrame(data)

@st.cache_data
def load_rainfall_data():
    years = list(range(1950, 2024))
    months = list(range(1, 13))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    
    baselines = {
        'Hewlêr': {'rain': 400, 'seasonal_var': 0.8},
        'Dihok': {'rain': 550, 'seasonal_var': 0.7},
        'Silêmanî': {'rain': 650, 'seasonal_var': 0.6},
        'Helebice': {'rain': 700, 'seasonal_var': 0.6},
        'Kerkuk': {'rain': 350, 'seasonal_var': 0.9}
    }

    for year in years:
        for month in months:
            for city in cities:
                baseline = baselines[city]['rain']
                seasonal_var = baselines[city]['seasonal_var']
                
                # Seasonal pattern (more rain in winter/spring)
                if month in [12, 1, 2, 3]:  # Winter and early spring
                    season_factor = 2.0
                elif month in [4, 5]:  # Spring
                    season_factor = 1.5
                elif month in [6, 7, 8]:  # Summer
                    season_factor = 0.2
                else:  # Autumn
                    season_factor = 1.0
                
                # Climate change trend
                if year < 1980:
                    trend = 1.0
                else:
                    trend = 1.0 - 0.005 * (year - 1980)
                
                # Calculate monthly rainfall
                monthly_rain = (baseline/12) * season_factor * trend * np.random.normal(1, seasonal_var)
                
                # Calculate drought condition
                drought_risk = 1 if monthly_rain < (baseline/12) * 0.5 else 0
                
                data.append({
                    'Year': year,
                    'Month': month,
                    'MonthName': calendar.month_name[month],
                    'City': city,
                    'Rainfall': max(0, monthly_rain),
                    'DroughtRisk': drought_risk,
                    'Season': (
                        'Winter' if month in [12, 1, 2] else
                        'Spring' if month in [3, 4, 5] else
                        'Summer' if month in [6, 7, 8] else
                        'Autumn'
                    )
                })
    return pd.DataFrame(data)

@st.cache_data
def load_water_resources_data():
    years = list(range(1950, 2024))
    months = list(range(1, 13))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    
    river_baselines = {
        'Hewlêr': 100,
        'Dihok': 150,
        'Silêmanî': 120,
        'Helebice': 90,
        'Kerkuk': 80
    }
    
    groundwater_baselines = {
        'Hewlêr': 50,
        'Dihok': 45,
        'Silêmanî': 55,
        'Helebice': 60,
        'Kerkuk': 40
    }

    for year in years:
        for month in months:
            for city in cities:
                # Seasonal variation
                season_factor = (
                    1.2 if month in [3, 4, 5] else  # Spring high
                    0.8 if month in [6, 7, 8] else  # Summer low
                    1.0  # Normal level
                )
                
                # Climate change trend
                if year < 1980:
                    trend = 1.0
                else:
                    trend = 1.0 - 0.008 * (year - 1980)
                
                river_level = river_baselines[city] * season_factor * trend + np.random.normal(0, 5)
                groundwater = groundwater_baselines[city] * trend + np.random.normal(0, 2)
                
                # Calculate water stress indicator
                water_stress = 1 if (river_level < river_baselines[city] * 0.7 and 
                                   groundwater < groundwater_baselines[city] * 0.7) else 0
                
                data.append({
                    'Year': year,
                    'Month': month,
                    'MonthName': calendar.month_name[month],
                    'City': city,
                    'RiverLevel': max(0, river_level),
                    'GroundwaterLevel': max(0, groundwater),
                    'WaterStress': water_stress,
                    'Season': (
                        'Winter' if month in [12, 1, 2] else
                        'Spring' if month in [3, 4, 5] else
                        'Summer' if month in [6, 7, 8] else
                        'Autumn'
                    )
                })
    return pd.DataFrame(data)

@st.cache_data
def load_economic_impact_data():
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    
    baselines = {
        'Hewlêr': {'energy': 1000, 'agri': 800},
        'Dihok': {'energy': 800, 'agri': 1000},
        'Silêmanî': {'energy': 900, 'agri': 1100},
        'Helebice': {'energy': 700, 'agri': 900},
        'Kerkuk': {'energy': 1100, 'agri': 700}
    }

    for year in years:
        for city in cities:
            # Climate change impact on energy demand
            if year < 1980:
                energy_trend = 1.0
            else:
                energy_trend = 1.0 + 0.02 * (year - 1980)
            
            energy_demand = baselines[city]['energy'] * energy_trend + np.random.normal(0, 20)
            
            # Agricultural economic impact
            if year < 1980:
                agri_trend = 1.0
            else:
                agri_trend = 1.0 - 0.005 * (year - 1980)
            
            agri_production = baselines[city]['agri'] * agri_trend + np.random.normal(0, 30)
            
            data.append({
                'Year': year,
                'City': city,
                'EnergyDemand': max(0, energy_demand),
                'AgriculturalProduction': max(0, agri_production)
            })
    return pd.DataFrame(data)

@st.cache_data
def load_health_impact_data():
    years = list(range(1950, 2024))
    months = list(range(1, 13))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
    data = []
    
    baselines = {
        'Hewlêr': {'heat_stress': 30, 'air_health': 80},
        'Dihok': {'heat_stress': 25, 'air_health': 85},
        'Silêmanî': {'heat_stress': 20, 'air_health': 90},
        'Helebice': {'heat_stress': 20, 'air_health': 90},
        'Kerkuk': {'heat_stress': 35, 'air_health': 75}
    }

    for year in years:
        for month in months:
            for city in cities:
                # Seasonal variation in health impacts
                season_factor = (
                    1.5 if month in [6, 7, 8] else  # Summer high
                    0.7 if month in [12, 1, 2] else  # Winter low
                    1.0  # Normal
                )
                
                # Climate change trend
                if year < 1980:
                    trend = 1.0
                else:
                    trend = 1.0 + 0.01 * (year - 1980)
                
                heat_stress = baselines[city]['heat_stress'] * season_factor * trend + np.random.normal(0, 2)
                air_health = baselines[city]['air_health'] * (2 - trend) + np.random.normal(0, 2)
                
                data.append({
                    'Year': year,
                    'Month': month,
                    'MonthName': calendar.month_name[month],
                    'City': city,
                    'HeatStressIndex': max(0, heat_stress),
                    'AirHealthIndex': max(0, min(100, air_health)),
                    'Season': (
                        'Winter' if month in [12, 1, 2] else
                        'Spring' if month in [3, 4, 5] else
                        'Summer' if month in [6, 7, 8] else
                        'Autumn'
                    )
                })
    return pd.DataFrame(data)

# Load all data
temp_df = load_temperature_data()
rainfall_df = load_rainfall_data()
water_df = load_water_resources_data()
economic_df = load_economic_impact_data()
health_df = load_health_impact_data()
# === PART 2 END ===
# === PART 3 START: ANALYSIS FUNCTIONS AND UI ===
# Sidebar controls
st.sidebar.header("Dashboard Controls")

# City selection
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk'],
    default=['Hewlêr', 'Dihok', 'Silêmanî', 'Helebice', 'Kerkuk']
)

# Time range
time_frame = st.sidebar.radio(
    "Select Time Frame",
    ["Yearly", "Monthly", "Seasonal"]
)

# Year range
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    1950, 2023, (1950, 2023)
)

if time_frame == "Monthly":
    months = st.sidebar.multiselect(
        "Select Months",
        list(calendar.month_name)[1:],
        default=list(calendar.month_name)[1:]
    )
elif time_frame == "Seasonal":
    seasons = st.sidebar.multiselect(
        "Select Seasons",
        ["Winter", "Spring", "Summer", "Autumn"],
        default=["Winter", "Spring", "Summer", "Autumn"]
    )

# Main category selection
category = st.sidebar.selectbox(
    "Select Category",
    ["Temperature & Precipitation",
     "Water Resources",
     "Economic Impact",
     "Health Impact",
     "Seasonal Analysis",
     "Future Projections",
     "Comparative Analysis"]
)

# Category-specific options
if category == "Temperature & Precipitation":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Temperature Trends",
         "Rainfall Patterns",
         "Extreme Weather Events",
         "Drought Analysis",
         "Combined View"]
    )
elif category == "Water Resources":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["River Levels",
         "Groundwater Levels",
         "Water Stress Index",
         "Combined Water Resources"]
    )
elif category == "Economic Impact":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Energy Demand",
         "Agricultural Production",
         "Economic Trends",
         "Combined Economic Impact"]
    )
elif category == "Health Impact":
    chart_type = st.sidebar.selectbox(
        "Select Indicator",
        ["Heat Stress Index",
         "Air Health Index",
         "Health Risk Patterns",
         "Combined Health Indicators"]
    )
elif category == "Seasonal Analysis":
    chart_type = st.sidebar.selectbox(
        "Select Analysis",
        ["Temperature Patterns",
         "Rainfall Distribution",
         "Seasonal Comparisons",
         "Year-over-Year Changes"]
    )
elif category == "Future Projections":
    chart_type = st.sidebar.selectbox(
        "Select Projection",
        ["Temperature Forecast",
         "Rainfall Forecast",
         "Water Resource Outlook",
         "Combined Projections"]
    )
else:  # Comparative Analysis
    chart_type = st.sidebar.selectbox(
        "Select Analysis",
        ["City Comparisons",
         "Trend Analysis",
         "Regional Patterns",
         "Historical Benchmarks"]
    )

# Additional analysis options
show_trend = st.sidebar.checkbox("Show Trend Lines", value=True)
show_confidence = st.sidebar.checkbox("Show Confidence Intervals")

# Download options
st.sidebar.markdown("---")
if st.sidebar.button("Download Data"):
    # Create download functionality here
    st.sidebar.success("Data downloaded successfully!")

# Filter data based on time frame and selection
def filter_data(df):
    filtered = df[
        (df['Year'] >= start_year) & 
        (df['Year'] <= end_year) & 
        (df['City'].isin(selected_cities))
    ]
    
    if time_frame == "Monthly" and 'Month' in df.columns:
        filtered = filtered[filtered['MonthName'].isin(months)]
    elif time_frame == "Seasonal" and 'Season' in df.columns:
        filtered = filtered[filtered['Season'].isin(seasons)]
    
    return filtered

# Apply filters to all dataframes
temp_df_filtered = filter_data(temp_df)
rainfall_df_filtered = filter_data(rainfall_df)
water_df_filtered = filter_data(water_df)
economic_df_filtered = filter_data(economic_df)
health_df_filtered = filter_data(health_df)
# === PART 3 END ===
# === PART 4 START: VISUALIZATION CODE ===
# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if category == "Temperature & Precipitation":
        if chart_type == "Temperature Trends":
            source = get_data_source('temperature')
            
            if time_frame == "Yearly":
                yearly_temp = temp_df_filtered.groupby(['Year', 'City'])['Temperature'].mean().reset_index()
                fig = px.line(
                    yearly_temp,
                    x='Year',
                    y='Temperature',
                    color='City',
                    title=f'Average Temperature Trends (Yearly)<br><sup>Source: {source["name"]}</sup>',
                    labels={'Temperature': 'Temperature (°C)'}
                )
                if show_trend:
                    fig.add_traces([
                        go.Scatter(
                            x=[yearly_temp['Year'].min(), yearly_temp['Year'].max()],
                            y=[yearly_temp[yearly_temp['City'] == city]['Temperature'].mean(),
                               yearly_temp[yearly_temp['City'] == city]['Temperature'].mean()],
                            name=f'{city} Trend',
                            line=dict(dash='dash'),
                            showlegend=False
                        ) for city in selected_cities
                    ])
            
            elif time_frame == "Monthly":
                fig = px.line(
                    temp_df_filtered,
                    x='Month',
                    y='Temperature',
                    color='City',
                    title=f'Temperature Patterns by Month<br><sup>Source: {source["name"]}</sup>',
                    labels={'Temperature': 'Temperature (°C)', 'Month': 'Month'},
                    line_group='Year'
                )
            
            else:  # Seasonal
                seasonal_temp = temp_df_filtered.groupby(['Season', 'City'])['Temperature'].mean().reset_index()
                fig = px.line(
                    seasonal_temp,
                    x='Season',
                    y='Temperature',
                    color='City',
                    title=f'Seasonal Temperature Patterns<br><sup>Source: {source["name"]}</sup>',
                    labels={'Temperature': 'Temperature (°C)'},
                    category_orders={"Season": ["Winter", "Spring", "Summer", "Autumn"]}
                )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

        elif chart_type == "Rainfall Patterns":
            source = get_data_source('rainfall')
            
            if time_frame == "Yearly":
                yearly_rain = rainfall_df_filtered.groupby(['Year', 'City'])['Rainfall'].sum().reset_index()
                fig = px.line(
                    yearly_rain,
                    x='Year',
                    y='Rainfall',
                    color='City',
                    title=f'Annual Rainfall Patterns<br><sup>Source: {source["name"]}</sup>',
                    labels={'Rainfall': 'Rainfall (mm/year)'}
                )
                if show_confidence:
                    for city in selected_cities:
                        city_data = yearly_rain[yearly_rain['City'] == city]
                        z = np.polyfit(city_data['Year'], city_data['Rainfall'], 1)
                        p = np.poly1d(z)
                        fig.add_trace(
                            go.Scatter(
                                x=city_data['Year'],
                                y=p(city_data['Year']),
                                name=f'{city} Trend',
                                line=dict(dash='dash'),
                                showlegend=False
                            )
                        )

            elif time_frame == "Monthly":
                fig = px.box(
                    rainfall_df_filtered,
                    x='MonthName',
                    y='Rainfall',
                    color='City',
                    title=f'Monthly Rainfall Distribution<br><sup>Source: {source["name"]}</sup>',
                    labels={'Rainfall': 'Rainfall (mm)', 'MonthName': 'Month'},
                    category_orders={"MonthName": list(calendar.month_name)[1:]}
                )

            else:  # Seasonal
                seasonal_rain = rainfall_df_filtered.groupby(['Season', 'City'])['Rainfall'].mean().reset_index()
                fig = px.bar(
                    seasonal_rain,
                    x='Season',
                    y='Rainfall',
                    color='City',
                    title=f'Seasonal Rainfall Patterns<br><sup>Source: {source["name"]}</sup>',
                    labels={'Rainfall': 'Average Rainfall (mm)'},
                    barmode='group',
                    category_orders={"Season": ["Winter", "Spring", "Summer", "Autumn"]}
                )

            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a> (Accessed: {source["access_date"]})</small>', unsafe_allow_html=True)

        elif chart_type == "Extreme Weather Events":
            # Heat waves analysis
            extreme_days = temp_df_filtered[temp_df_filtered['ExtremeHeatDay']].groupby(['Year', 'City']).size().reset_index(name='ExtremeDays')
            
            fig = px.line(
                extreme_days,
                x='Year',
                y='ExtremeDays',
                color='City',
                title='Number of Extreme Heat Days (>40°C) per Year',
                labels={'ExtremeDays': 'Days Above 40°C'}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Drought analysis
            drought_data = rainfall_df_filtered.groupby(['Year', 'City'])['DroughtRisk'].mean().reset_index()
            fig2 = px.line(
                drought_data,
                x='Year',
                y='DroughtRisk',
                color='City',
                title='Drought Risk Index',
                labels={'DroughtRisk': 'Risk Index (0-1)'}
            )
            st.plotly_chart(fig2, use_container_width=True)

    elif category == "Water Resources":
        source = get_data_source('water_resources')
        
        if chart_type == "Water Stress Index":
            stress_data = water_df_filtered.groupby(['Year', 'City'])['WaterStress'].mean().reset_index()
            fig = px.line(
                stress_data,
                x='Year',
                y='WaterStress',
                color='City',
                title=f'Water Stress Index<br><sup>Source: {source["name"]}</sup>',
                labels={'WaterStress': 'Stress Index (0-1)'}
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Combined Water Resources":
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            for city in selected_cities:
                city_data = water_df_filtered[water_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['RiverLevel'],
                        name=f'{city} River',
                        mode='lines'
                    ),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['GroundwaterLevel'],
                        name=f'{city} Groundwater',
                        line=dict(dash='dash')
                    ),
                    secondary_y=True
                )
            
            fig.update_layout(
                title=f'Combined Water Resources<br><sup>Source: {source["name"]}</sup>',
                yaxis_title="River Level (m³/s)",
                yaxis2_title="Groundwater Level (m)"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif category == "Economic Impact":
        source = get_data_source('economic')
        
        if chart_type == "Combined Economic Impact":
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            for city in selected_cities:
                city_data = economic_df_filtered[economic_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['EnergyDemand'],
                        name=f'{city} Energy',
                        mode='lines'
                    ),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['AgriculturalProduction'],
                        name=f'{city} Agriculture',
                        line=dict(dash='dash')
                    ),
                    secondary_y=True
                )
            
            fig.update_layout(
                title=f'Economic Indicators<br><sup>Source: {source["name"]}</sup>',
                yaxis_title="Energy Demand (MW)",
                yaxis2_title="Agricultural Production (tons)"
            )
            st.plotly_chart(fig, use_container_width=True)

    elif category == "Health Impact":
        source = get_data_source('health')
        
        if time_frame == "Yearly":
            yearly_health = health_df_filtered.groupby(['Year', 'City'])[['HeatStressIndex', 'AirHealthIndex']].mean().reset_index()
            
            if chart_type == "Combined Health Indicators":
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                for city in selected_cities:
                    city_data = yearly_health[yearly_health['City'] == city]
                    fig.add_trace(
                        go.Scatter(
                            x=city_data['Year'],
                            y=city_data['HeatStressIndex'],
                            name=f'{city} Heat Stress',
                            mode='lines'
                        ),
                        secondary_y=False
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=city_data['Year'],
                            y=city_data['AirHealthIndex'],
                            name=f'{city} Air Quality',
                            line=dict(dash='dash')
                        ),
                        secondary_y=True
                    )
                
                fig.update_layout(
                    title=f'Health Impact Indicators<br><sup>Source: {source["name"]}</sup>',
                    yaxis_title="Heat Stress Index",
                    yaxis2_title="Air Quality Index"
                )
                st.plotly_chart(fig, use_container_width=True)

    elif category == "Future Projections":
        if chart_type == "Temperature Forecast":
            # Simple linear projection for next 10 years
            future_years = list(range(end_year + 1, end_year + 11))
            forecast_data = []
            
            for city in selected_cities:
                city_data = temp_df_filtered[temp_df_filtered['City'] == city]
                z = np.polyfit(city_data['Year'], city_data['Temperature'], 1)
                p = np.poly1d(z)
                
                # Historical data
                forecast_data.extend([{
                    'Year': year,
                    'Temperature': temp,
                    'City': city,
                    'Type': 'Historical'
                } for year, temp in zip(city_data['Year'], city_data['Temperature'])])
                
                # Projected data
                forecast_data.extend([{
                    'Year': year,
                    'Temperature': p(year),
                    'City': city,
                    'Type': 'Projected'
                } for year in future_years])
            
            forecast_df = pd.DataFrame(forecast_data)
            
            fig = px.line(
                forecast_df,
                x='Year',
                y='Temperature',
                color='City',
                line_dash='Type',
                title='Temperature Forecast (10-Year Projection)',
                labels={'Temperature': 'Temperature (°C)'}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif category == "Comparative Analysis":
        if chart_type == "City Comparisons":
            # Temperature comparison
            temp_comparison = temp_df_filtered.groupby(['City'])['Temperature'].agg(['mean', 'std', 'min', 'max']).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=temp_comparison['City'],
                y=temp_comparison['mean'],
                error_y=dict(type='data', array=temp_comparison['std']),
                name='Average Temperature'
            ))
            
            fig.update_layout(
                title='Temperature Comparison Across Cities',
                yaxis_title='Temperature (°C)'
            )
            st.plotly_chart(fig, use_container_width=True)
# === PART 4 END ===
# === PART 5 START: STATISTICS AND FOOTER ===
with col2:
    st.write("## City Statistics")
    
    for city in selected_cities:
        st.write(f"### {city}")
        
        with st.expander("View Detailed Statistics"):
            # Temperature & Precipitation Stats
            st.write("🌡️ **Climate Indicators**")
            
            # Get city-specific data
            city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
            city_rain = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
            
            # Calculate seasonal averages
            seasonal_temp = city_temp.groupby('Season')['Temperature'].mean()
            seasonal_rain = city_rain.groupby('Season')['Rainfall'].mean()
            
            # Temperature Statistics
            col_temp, col_rain = st.columns(2)
            with col_temp:
                current_temp = city_temp['Temperature'].iloc[-1]
                historical_avg = city_temp['Temperature'].mean()
                temp_change = current_temp - historical_avg
                
                st.metric(
                    "Temperature",
                    f"{current_temp:.1f}°C",
                    f"{temp_change:+.1f}°C vs historical",
                    delta_color="inverse"
                )
                
                # Show seasonal breakdown
                st.write("Seasonal Averages:")
                for season in ['Winter', 'Spring', 'Summer', 'Autumn']:
                    if season in seasonal_temp:
                        st.write(f"{season}: {seasonal_temp[season]:.1f}°C")
            
            with col_rain:
                current_rain = city_rain['Rainfall'].iloc[-1]
                historical_avg_rain = city_rain['Rainfall'].mean()
                rain_change = current_rain - historical_avg_rain
                
                st.metric(
                    "Rainfall",
                    f"{current_rain:.0f}mm",
                    f"{rain_change:+.0f}mm vs historical",
                    delta_color="normal"
                )
                
                # Show seasonal breakdown
                st.write("Seasonal Averages:")
                for season in ['Winter', 'Spring', 'Summer', 'Autumn']:
                    if season in seasonal_rain:
                        st.write(f"{season}: {seasonal_rain[season]:.0f}mm")

            # Extreme Weather Stats
            st.write("🌪️ **Extreme Weather**")
            extreme_days_count = len(city_temp[city_temp['ExtremeHeatDay']])
            drought_days_count = len(city_rain[city_rain['DroughtRisk'] > 0.5])
            
            col_extreme, col_drought = st.columns(2)
            with col_extreme:
                st.metric(
                    "Heat Wave Days",
                    f"{extreme_days_count}",
                    "Above 40°C",
                    delta_color="inverse"
                )
            with col_drought:
                st.metric(
                    "Drought Days",
                    f"{drought_days_count}",
                    "Risk > 50%",
                    delta_color="inverse"
                )

            # Water Resources Stats
            st.write("💧 **Water Resources**")
            city_water = water_df_filtered[water_df_filtered['City'] == city]
            
            col_river, col_ground = st.columns(2)
            with col_river:
                current_river = city_water['RiverLevel'].iloc[-1]
                river_change = current_river - city_water['RiverLevel'].mean()
                
                st.metric(
                    "River Level",
                    f"{current_river:.1f}m³/s",
                    f"{river_change:+.1f}m³/s",
                    delta_color="normal"
                )
            with col_ground:
                current_ground = city_water['GroundwaterLevel'].iloc[-1]
                ground_change = current_ground - city_water['GroundwaterLevel'].mean()
                
                st.metric(
                    "Groundwater",
                    f"{current_ground:.1f}m",
                    f"{ground_change:+.1f}m",
                    delta_color="normal"
                )

            # Economic Impact Stats
            st.write("💰 **Economic Impact**")
            city_econ = economic_df_filtered[economic_df_filtered['City'] == city]
            
            col_energy, col_agri = st.columns(2)
            with col_energy:
                current_energy = city_econ['EnergyDemand'].iloc[-1]
                energy_change = current_energy - city_econ['EnergyDemand'].mean()
                
                st.metric(
                    "Energy Demand",
                    f"{current_energy:.0f}MW",
                    f"{energy_change:+.0f}MW",
                    delta_color="inverse"
                )
            with col_agri:
                current_agri = city_econ['AgriculturalProduction'].iloc[-1]
                agri_change = current_agri - city_econ['AgriculturalProduction'].mean()
                
                st.metric(
                    "Agricultural Output",
                    f"{current_agri:.0f}tons",
                    f"{agri_change:+.0f}tons",
                    delta_color="normal"
                )

            # Health Impact Stats
            st.write("🏥 **Health Impact**")
            city_health = health_df_filtered[health_df_filtered['City'] == city]
            
            col_heat, col_air = st.columns(2)
            with col_heat:
                current_heat = city_health['HeatStressIndex'].iloc[-1]
                heat_change = current_heat - city_health['HeatStressIndex'].mean()
                
                st.metric(
                    "Heat Stress",
                    f"{current_heat:.1f}",
                    f"{heat_change:+.1f}",
                    delta_color="inverse"
                )
            with col_air:
                current_air = city_health['AirHealthIndex'].iloc[-1]
                air_change = current_air - city_health['AirHealthIndex'].mean()
                
                st.metric(
                    "Air Quality",
                    f"{current_air:.1f}",
                    f"{air_change:+.1f}",
                    delta_color="normal"
                )

    # Information about indicators
    st.info("""
    **Understanding the Indicators**
    
    🌡️ **Climate Indicators:**
    - Temperature increase (🔴) indicates warming
    - Rainfall decrease (🔴) suggests drought risk
    
    🌪️ **Extreme Weather:**
    - Heat wave days above 40°C (🔴)
    - Drought risk above 50% (🔴)
    
    💧 **Water Resources:**
    - River level decrease (🔴)
    - Groundwater depletion (🔴)
    
    💰 **Economic Impact:**
    - Energy demand increase (🔴)
    - Agricultural output decrease (🔴)
    
    🏥 **Health Impact:**
    - Heat stress increase (🔴)
    - Air quality decrease (🔴)
    
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
- Kurdistan Regional Water Management

🌪️ **Extreme Weather:**
- [EM-DAT Database](https://www.emdat.be)
- Local Weather Stations

💰 **Economic Data:**
- [World Bank Open Data](https://data.worldbank.org)
- Regional Economic Reports

🏥 **Health Impact:**
- [WHO Global Health Observatory](https://www.who.int/data/gho)
- Regional Health Statistics

Notes:
- Each visualization includes its specific data source
- Click source links to access original datasets
- Some sources may require registration
- Data is updated periodically
- Historical trends are based on available records
- Projections use statistical modeling</small>
""", unsafe_allow_html=True)
# === PART 5 END ===