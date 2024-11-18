# climate_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Climate Change Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Climate Change Dashboard")
st.markdown("""
This dashboard visualizes various climate change indicators and metrics.
Data is for demonstration purposes - replace with real climate data sources.
""")

# Sample data generation (replace with real data)
@st.cache_data
def load_temperature_data():
    # Simulated global temperature anomaly data
    years = list(range(1900, 2024))
    temp_anomaly = [0.1 * (year - 1900) + np.random.normal(0, 0.2) for year in years]
    return pd.DataFrame({
        'Year': years,
        'Temperature_Anomaly': temp_anomaly
    })

@st.cache_data
def load_emissions_data():
    # Simulated CO2 emissions data
    years = list(range(1900, 2024))
    emissions = [2000 * np.exp(0.02 * (year - 1900)) + np.random.normal(0, 1000) for year in years]
    return pd.DataFrame({
        'Year': years,
        'CO2_Emissions': emissions
    })

# Load data
temp_df = load_temperature_data()
emissions_df = load_emissions_data()

# Sidebar for controls
st.sidebar.header("Dashboard Controls")
start_year = st.sidebar.slider("Select Start Year", 1900, 2023, 1900)
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Temperature Anomalies", "CO2 Emissions", "Combined View"]
)

# Filter data based on selected year
temp_df_filtered = temp_df[temp_df['Year'] >= start_year]
emissions_df_filtered = emissions_df[emissions_df['Year'] >= start_year]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if chart_type == "Temperature Anomalies":
        fig = px.line(
            temp_df_filtered,
            x='Year',
            y='Temperature_Anomaly',
            title='Global Temperature Anomalies Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "CO2 Emissions":
        fig = px.line(
            emissions_df_filtered,
            x='Year',
            y='CO2_Emissions',
            title='Global CO2 Emissions Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Combined View
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=temp_df_filtered['Year'],
                y=temp_df_filtered['Temperature_Anomaly'],
                name='Temperature Anomaly',
                yaxis='y1'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=emissions_df_filtered['Year'],
                y=emissions_df_filtered['CO2_Emissions'],
                name='CO2 Emissions',
                yaxis='y2'
            )
        )
        fig.update_layout(
            title='Combined Climate Indicators',
            yaxis=dict(title='Temperature Anomaly (°C)'),
            yaxis2=dict(title='CO2 Emissions (Mt)', overlaying='y', side='right')
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Key Statistics")
    
    # Calculate and display key metrics
    latest_temp = temp_df_filtered['Temperature_Anomaly'].iloc[-1]
    temp_change = temp_df_filtered['Temperature_Anomaly'].iloc[-1] - \
                 temp_df_filtered['Temperature_Anomaly'].iloc[0]
    
    latest_emissions = emissions_df_filtered['CO2_Emissions'].iloc[-1]
    emissions_change = emissions_df_filtered['CO2_Emissions'].iloc[-1] - \
                      emissions_df_filtered['CO2_Emissions'].iloc[0]
    
    st.metric(
        "Current Temperature Anomaly",
        f"{latest_temp:.2f}°C",
        f"{temp_change:+.2f}°C since {start_year}"
    )
    
    st.metric(
        "Current Annual CO2 Emissions",
        f"{latest_emissions:.0f} Mt",
        f"{emissions_change:+.0f} Mt since {start_year}"
    )

    # Add additional information
    st.info("""
    **About this Dashboard**
    
    This dashboard shows key climate indicators:
    - Temperature anomalies relative to pre-industrial levels
    - Annual CO2 emissions
    - Combined view for correlation analysis
    
    Use the sidebar controls to adjust the view and time period.
    """)

# Footer
st.markdown("---")
st.markdown("""
<small>Data sources: Sample data for demonstration. Replace with real climate data from sources like:
- NASA GISS Surface Temperature Analysis
- Global Carbon Project
- NOAA Climate Data</small>
""", unsafe_allow_html=True)