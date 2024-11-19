import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Kurdistan Cities Climate Dashboard (1950-Present)",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Kurdistan Cities Climate Dashboard (1950-Present)")
st.markdown("""
This dashboard visualizes historical climate change indicators for major cities in Kurdistan Region from 1950 onwards:
- Hewlêr (Erbil)
- Duhok
- Silêmanî (Sulaymaniyah)
- Halabja
""")

# Sample data generation for Kurdistan cities
@st.cache_data
def load_temperature_data():
    # Simulated temperature data for Kurdistan cities from 1950
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Duhok', 'Silêmanî', 'Halabja']
    
    data = []
    # Historical baseline temperatures for each city
    baselines = {
        'Hewlêr': 33,     # Historical baseline for Hewlêr (Erbil)
        'Duhok': 31,      # Historically cooler in Duhok
        'Silêmanî': 30,   # Cooler due to elevation
        'Halabja': 29     # Coolest due to highest elevation
    }
    
    for year in years:
        for city in cities:
            baseline = baselines[city]
            # Add historical trend and random variation
            # Stronger warming trend after 1980
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
    # Simulated rainfall data for Kurdistan cities
    years = list(range(1950, 2024))
    cities = ['Hewlêr', 'Duhok', 'Silêmanî', 'Halabja']
    
    data = []
    # Historical rainfall patterns for each city
    baselines = {
        'Hewlêr': 400,    # Annual rainfall in mm
        'Duhok': 550,     # Higher rainfall in Duhok
        'Silêmanî': 650,  # High rainfall due to mountains
        'Halabja': 700    # Highest rainfall due to location
    }
    
    for year in years:
        for city in cities:
            baseline = baselines[city]
            # Add yearly trend (decrease after 1980) and random variation
            if year < 1980:
                trend = 1.0
            else:
                trend = 1.0 - 0.005 * (year - 1980)
            rainfall = baseline * trend + np.random.normal(0, 30)
            data.append({
                'Year': year,
                'City': city,
                'Rainfall': max(0, rainfall)  # Ensure non-negative rainfall
            })
    
    return pd.DataFrame(data)

# Load data
temp_df = load_temperature_data()
rainfall_df = load_rainfall_data()

# Sidebar controls
st.sidebar.header("Dashboard Controls")
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    ['Hewlêr', 'Duhok', 'Silêmanî', 'Halabja'],
    default=['Hewlêr', 'Duhok', 'Silêmanî', 'Halabja']
)

start_year = st.sidebar.slider("Select Start Year", 1950, 2023, 1950)
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Temperature Trends", "Rainfall Patterns", "Combined View"]
)

# Filter data
temp_df_filtered = temp_df[
    (temp_df['Year'] >= start_year) & 
    (temp_df['City'].isin(selected_cities))
]
rainfall_df_filtered = rainfall_df[
    (rainfall_df['Year'] >= start_year) & 
    (rainfall_df['City'].isin(selected_cities))
]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if chart_type == "Temperature Trends":
        fig = px.line(
            temp_df_filtered,
            x='Year',
            y='Temperature',
            color='City',
            title='Average Temperature Trends in Kurdistan Cities',
            labels={'Temperature': 'Temperature (°C)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Rainfall Patterns":
        fig = px.line(
            rainfall_df_filtered,
            x='Year',
            y='Rainfall',
            color='City',
            title='Annual Rainfall Patterns in Kurdistan Cities',
            labels={'Rainfall': 'Rainfall (mm/year)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Combined View
        fig = go.Figure()
        
        # Add temperature traces
        for city in selected_cities:
            city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
            fig.add_trace(
                go.Scatter(
                    x=city_temp['Year'],
                    y=city_temp['Temperature'],
                    name=f'{city} Temperature',
                    yaxis='y1',
                    line=dict(dash='solid')
                )
            )
        
        # Add rainfall traces
        for city in selected_cities:
            city_rain = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
            fig.add_trace(
                go.Scatter(
                    x=city_rain['Year'],
                    y=city_rain['Rainfall'],
                    name=f'{city} Rainfall',
                    yaxis='y2',
                    line=dict(dash='dot')
                )
            )
            
        fig.update_layout(
            title='Combined Temperature and Rainfall Trends in Kurdistan Cities',
            yaxis=dict(title='Temperature (°C)', titlefont=dict(color='#FF4B4B')),
            yaxis2=dict(
                title='Rainfall (mm/year)',
                titlefont=dict(color='#1F77B4'),
                overlaying='y',
                side='right'
            )
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("City Statistics")
    
    for city in selected_cities:
        st.write(f"### {city}")
        
        # Temperature statistics
        city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
        latest_temp = city_temp['Temperature'].iloc[-1]
        temp_change = city_temp['Temperature'].iloc[-1] - city_temp['Temperature'].iloc[0]
        
        # Rainfall statistics
        city_rain = rainfall_df_filtered[rainfall_df_filtered['City'] == city]
        latest_rain = city_rain['Rainfall'].iloc[-1]
        rain_change = city_rain['Rainfall'].iloc[-1] - city_rain['Rainfall'].iloc[0]
        
        # Display metrics
        col_temp, col_rain = st.columns(2)
        with col_temp:
            st.metric(
                "Temperature",
                f"{latest_temp:.1f}°C",
                f"{temp_change:+.1f}°C"
            )
        with col_rain:
            st.metric(
                "Rainfall",
                f"{latest_rain:.0f}mm",
                f"{rain_change:+.0f}mm"
            )

    # Add information about the data
    st.info("""
    **About this Dashboard**
    
    This dashboard shows historical climate trends for major Kurdistan cities:
    - Historical temperature trends since 1950
    - Annual rainfall patterns
    - Combined analysis showing climate change impacts
    
    Note: This uses simulated data. For accurate local data, connect to:
    - Kurdistan Region Statistics Office
    - Local meteorological stations
    - Regional climate research centers
    """)

# Footer
st.markdown("---")
st.markdown("""
<small>💡 To get real climate data for Kurdistan cities, you would need to:
- Access Kurdistan Region meteorological databases
- Connect to local weather stations
- Use satellite data from climate monitoring services
- Partner with Kurdish universities and research centers</small>
""", unsafe_allow_html=True)