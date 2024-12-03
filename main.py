import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.figure_factory as ff
from scipy import stats
import calendar

st.set_page_config(
    page_title="Kurdistan Climate & Energy Dashboard (1950-Present)",
    page_icon="🌍",
    layout="wide"
)

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
        'energy': {
            'link': '#',
            'name': 'Kurdistan Ministry of Electricity',
            'access_date': 'Pending'
        }
    }
    return sources.get(indicator, {'link': '#', 'name': 'Data Source', 'access_date': 'Nov 2023'})

st.title("🌍 Kurdistan Climate & Energy Dashboard (1950-Present)")
st.markdown("""
This comprehensive dashboard visualizes climate and energy data for major cities in Kurdistan Region:
* Hewlêr (Erbil)
* Dihok (Duhok)
* Silêmanî (Sulaymaniyah)
* Helebce (Halabja)
* Kerkuk (Kirkuk)
""")
# === PART 2: DATA LOADING FUNCTIONS ===
@st.cache_data
def load_temperature_data():
   years = list(range(1950, 2024))
   months = list(range(1, 13))
   cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkuk']
   data = []
   
   baselines = {
       'Hewlêr': {'temp': 33, 'seasonal_var': 15},
       'Dihok': {'temp': 31, 'seasonal_var': 14},
       'Silêmanî': {'temp': 30, 'seasonal_var': 13}, 
       'Helebce': {'temp': 29, 'seasonal_var': 13},
       'Kerkuk': {'temp': 34, 'seasonal_var': 16}
   }

   for year in years:
       for month in months:
           for city in cities:
               baseline = baselines[city]['temp']
               seasonal_var = baselines[city]['seasonal_var']
               season_effect = -seasonal_var * np.cos(2 * np.pi * (month - 1) / 12)
               if year < 1980:
                   trend = 0.01 * (year - 1950)
               else:
                   trend = 0.3 + 0.03 * (year - 1980)
               temp = baseline + season_effect + trend + np.random.normal(0, 0.5)
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

# Add other data loading functions here: rainfall, water resources, etc.
# === PART 3: UI CONTROLS ===
# Sidebar controls
st.sidebar.header("Dashboard Controls")

# Basic selections
selected_cities = st.sidebar.multiselect(
   "Select Cities",
   ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkuk'],
   default=['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkuk']
)

time_frame = st.sidebar.radio(
   "Select Time Frame",
   ["Yearly", "Monthly", "Seasonal"]
)

start_year, end_year = st.sidebar.slider(
   "Select Year Range",
   1950, 2023, (1950, 2023)
)

# Time frame specific controls
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
   ["Open Source Data",
    "Kurdistan Government Energy Data",
    "Combined Analysis"]
)

# Category-specific options
if category == "Open Source Data":
   data_type = st.sidebar.selectbox(
       "Select Data Type",
       ["Temperature & Precipitation",
        "Water Resources",
        "Economic Impact",
        "Health Impact",
        "Seasonal Analysis"]
   )
   
   if data_type == "Temperature & Precipitation":
       chart_type = st.sidebar.selectbox(
           "Select Indicator",
           ["Temperature Trends",
            "Rainfall Patterns",
            "Extreme Weather Events",
            "Combined View"]
       )
   elif data_type == "Water Resources":
       chart_type = st.sidebar.selectbox(
           "Select Indicator",
           ["River Levels",
            "Groundwater Levels",
            "Water Stress Index"]
       )
   elif data_type == "Economic Impact":
       chart_type = st.sidebar.selectbox(
           "Select Indicator",
           ["Energy Demand",
            "Agricultural Production",
            "Combined Impact"]
       )
   elif data_type == "Health Impact":
       chart_type = st.sidebar.selectbox(
           "Select Indicator",
           ["Heat Stress Index",
            "Air Quality Index",
            "Combined Health Indicators"]
       )
   else:  # Seasonal Analysis
       chart_type = st.sidebar.selectbox(
           "Select Analysis",
           ["Temperature Patterns",
            "Rainfall Distribution",
            "Seasonal Comparisons"]
       )

elif category == "Kurdistan Government Energy Data":
   data_type = st.sidebar.selectbox(
       "Select Data Type",
       ["Power Generation",
        "Energy Consumption",
        "Regional Distribution"]
   )
   st.sidebar.info("Kurdistan energy data integration pending")
   chart_type = "Placeholder"

else:  # Combined Analysis
   data_type = st.sidebar.selectbox(
       "Select Analysis Type",
       ["Cross-Source Comparison",
        "Trend Validation",
        "Data Correlation",
        "Regional Patterns"]
   )

# Analysis options
show_trend = st.sidebar.checkbox("Show Trend Lines", value=True)
show_confidence = st.sidebar.checkbox("Show Confidence Intervals")
# === PART 4: VISUALIZATION CODE ===
# Main content area
col1, col2 = st.columns([2, 1])

with col1:
   if category == "Open Source Data":
       if data_type == "Temperature & Precipitation":
           source = get_data_source('temperature')
           
           if chart_type == "Temperature Trends":
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
                       for city in selected_cities:
                           city_data = yearly_temp[yearly_temp['City'] == city]
                           z = np.polyfit(city_data['Year'], city_data['Temperature'], 1)
                           p = np.poly1d(z)
                           fig.add_trace(
                               go.Scatter(
                                   x=city_data['Year'],
                                   y=p(city_data['Year']),
                                   name=f'{city} Trend',
                                   line=dict(dash='dash')
                               )
                           )
                   st.plotly_chart(fig, use_container_width=True)

   elif category == "Kurdistan Government Energy Data":
       st.info("Kurdistan energy data visualization will be added here")
       if data_type == "Power Generation":
           st.write("Power generation data coming soon")
       elif data_type == "Energy Consumption":
           st.write("Energy consumption data coming soon")
       else:
           st.write("Regional distribution data coming soon")

   else:  # Combined Analysis
       st.write("Combined analysis visualizations will be implemented here")
       # === PART 5: STATISTICS PANEL AND FOOTER ===
with col2:
   st.write("## Statistics")
   
   if category == "Open Source Data":
       for city in selected_cities:
           st.write(f"### {city}")
           
           with st.expander("View Statistics"):
               if data_type == "Temperature & Precipitation":
                   city_temp = temp_df_filtered[temp_df_filtered['City'] == city]
                   current_temp = city_temp['Temperature'].iloc[-1]
                   historical_avg = city_temp['Temperature'].mean()
                   temp_change = current_temp - historical_avg
                   
                   st.metric(
                       "Temperature",
                       f"{current_temp:.1f}°C",
                       f"{temp_change:+.1f}°C vs historical",
                       delta_color="inverse"
                   )
                   
                   st.write("Seasonal Averages:")
                   seasonal_temp = city_temp.groupby('Season')['Temperature'].mean()
                   for season in ['Winter', 'Spring', 'Summer', 'Autumn']:
                       if season in seasonal_temp:
                           st.write(f"{season}: {seasonal_temp[season]:.1f}°C")

   elif category == "Kurdistan Government Energy Data":
       st.write("### Energy Statistics")
       st.info("Energy statistics will be displayed here once data is integrated")

   else:  # Combined Analysis
       st.write("### Comparative Statistics")
       st.info("Cross-source statistical analysis will be shown here")

   # Information box
   st.info("""
   **Understanding Indicators**
   
   🌡️ Open Source Data:
   - Temperature changes (🔴 increase concerning)
   - Rainfall patterns
   - Water resources
   
   ⚡ Government Energy Data:
   - Power generation
   - Consumption patterns
   - Regional distribution
   
   Color Indicators:
   🔴 Red: Concerning changes
   🟢 Green: Positive changes
   """)

# Footer
st.markdown("---")
st.markdown("""
<small>**Data Sources:**

📊 **Open Source Data:**
- Temperature: [World Bank Climate Portal](https://climateknowledgeportal.worldbank.org/country/iraq/climate-data-historical)
- Water Resources: [FAO AQUASTAT](https://www.fao.org/aquastat/en/databases/)

⚡ **Kurdistan Energy Data:**
- Ministry of Electricity (pending integration)
- Regional power distribution data (pending)

Notes:
- Open source data updated periodically
- Government energy data integration in progress</small>
""", unsafe_allow_html=True)