import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Kurdistan Cities Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Iraq Cities Climate Dashboard")
st.markdown("""
This dashboard visualizes climate change indicators for major cities in Iraqi Kurdistan:
- Erbil
- Duhok
- Kirkuk
- Sulaymaniyah
""")

# Sample data generation for Iraqi cities
@st.cache_data
def load_temperature_data():
    # Simulated temperature data for Iraqi cities
    years = list(range(2000, 2024))
    cities = ['Erbil', 'Duhok', 'Kirkuk', 'Sulaymaniyah']
    
    data = []
    # Simulate different baseline temperatures and trends for each city
    baselines = {
        'Erbil': 35,      # Higher baseline for Erbil
        'Duhok': 33,      # Slightly cooler in Duhok
        'Kirkuk': 36,     # Warmest in Kirkuk
        'Sulaymaniyah': 32 # Coolest in Sulaymaniyah due to elevation
    }
    
    for year in years:
        for city in cities:
            baseline = baselines[city]
            # Add yearly trend and random variation
            temp = baseline + 0.04 * (year - 2000) + np.random.normal(0, 0.5)
            data.append({
                'Year': year,
                'City': city,
                'Temperature': temp
            })
    
    return pd.DataFrame(data)

@st.cache_data
def load_rainfall_data():
    # Simulated rainfall data for Iraqi cities
    years = list(range(2000, 2024))
    cities = ['Erbil', 'Duhok', 'Kirkuk', 'Sulaymaniyah']
    
    data = []
    # Simulate different rainfall patterns for each city
    baselines = {
        'Erbil': 400,      # Annual rainfall in mm
        'Duhok': 550,      # Higher rainfall in Duhok
        'Kirkuk': 350,     # Drier in Kirkuk
        'Sulaymaniyah': 650 # Highest rainfall in Sulaymaniyah
    }
    
    for year in years:
        for city in cities:
            baseline = baselines[city]
            # Add yearly trend (slight decrease) and random variation
            rainfall = baseline * (1 - 0.005 * (year - 2000)) + np.random.normal(0, 30)
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
    ['Erbil', 'Duhok', 'Kirkuk', 'Sulaymaniyah'],
    default=['Erbil', 'Duhok', 'Kirkuk', 'Sulaymaniyah']
)

start_year = st.sidebar.slider("Select Start Year", 2000, 2023, 2000)
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
            title='Average Temperature Trends by City',
            labels={'Temperature': 'Temperature (°C)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Rainfall Patterns":
        fig = px.line(
            rainfall_df_filtered,
            x='Year',
            y='Rainfall',
            color='City',
            title='Annual Rainfall Patterns by City',
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
            title='Combined Temperature and Rainfall Trends',
            yaxis=dict(title='Temperature (°C)', titlefont=dict(color='red')),
            yaxis2=dict(
                title='Rainfall (mm/year)',
                titlefont=dict(color='blue'),
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
    
    This dashboard shows climate trends for major Iraqi cities:
    - Temperature trends over time
    - Annual rainfall patterns
    - Combined view for correlation analysis
    
    Note: This uses simulated data. For accurate local data, connect to:
    - Iraqi Meteorological Organization
    - Kurdistan Region Statistics Office
    - Local weather stations
    """)

# Footer
st.markdown("---")
st.markdown("""
<small>💡 To get real climate data for these cities, you would need to:
- Connect to local weather stations
- Access Iraqi meteorological databases
- Use satellite data from climate monitoring services
- Partner with local environmental agencies</small>
""", unsafe_allow_html=True)