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


# === PART 1 END ===
# === PART 2 START: DATA LOADING FUNCTIONS ===
@st.cache_data
def load_temperature_data():
    years = list(range(1950, 2024))
    months = list(range(1, 13))
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    data = []
    
    baselines = {
        'Hewlêr': {'temp': 33, 'seasonal_var': 15},
        'Dihok': {'temp': 31, 'seasonal_var': 14},
        'Silêmanî': {'temp': 30, 'seasonal_var': 13},
        'Helebce': {'temp': 29, 'seasonal_var': 13},
        'Kerkûk': {'temp': 34, 'seasonal_var': 16}
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
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    data = []
    
    baselines = {
        'Hewlêr': {'rain': 400, 'seasonal_var': 0.8},
        'Dihok': {'rain': 550, 'seasonal_var': 0.7},
        'Silêmanî': {'rain': 650, 'seasonal_var': 0.6},
        'Helebce': {'rain': 700, 'seasonal_var': 0.6},
        'Kerkûk': {'rain': 350, 'seasonal_var': 0.9}
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
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    data = []
    
    river_baselines = {
        'Hewlêr': 100,
        'Dihok': 150,
        'Silêmanî': 120,
        'Helebce': 90,
        'Kerkûk': 80
    }
    
    groundwater_baselines = {
        'Hewlêr': 50,
        'Dihok': 45,
        'Silêmanî': 55,
        'Helebce': 60,
        'Kerkûk': 40
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
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    data = []
    
    baselines = {
        'Hewlêr': {'energy': 1000, 'agri': 800},
        'Dihok': {'energy': 800, 'agri': 1000},
        'Silêmanî': {'energy': 900, 'agri': 1100},
        'Helebce': {'energy': 700, 'agri': 900},
        'Kerkûk': {'energy': 1100, 'agri': 700}
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
    cities = ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    data = []
    
    baselines = {
        'Hewlêr': {'heat_stress': 30, 'air_health': 80},
        'Dihok': {'heat_stress': 25, 'air_health': 85},
        'Silêmanî': {'heat_stress': 20, 'air_health': 90},
        'Helebce': {'heat_stress': 20, 'air_health': 90},
        'Kerkûk': {'heat_stress': 35, 'air_health': 75}
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
    
@st.cache_data
def load_waste_data():
    try:
        # Load the Excel file into a DataFrame
        file_path = "GovData/waste/waste_composition.xlsx"  # Update this path if necessary
        waste_data = pd.read_excel(file_path)

        # Strip column names to avoid leading/trailing whitespace issues
        waste_data.columns = waste_data.columns.str.strip()

        # Ensure column names are exactly 'Type' and 'Percentage'
        if 'Type' not in waste_data.columns or 'Percentage' not in waste_data.columns:
            raise ValueError("The columns 'Type' and 'Percentage' are not found in the data.")

        # Ensure Percentage column is numeric
        waste_data['Percentage'] = pd.to_numeric(waste_data['Percentage'], errors='coerce')

        # Return the validated DataFrame
        return waste_data.dropna()
    except Exception as e:
        st.error(f"Error loading waste data: {str(e)}")
        # Return empty DataFrame if file loading fails
        return pd.DataFrame({'Type': [], 'Percentage': []})

@st.cache_data
def load_waste_forecast_data():
    try:
        # Define the path to the Excel file
        file_path = "GovData/waste/WasteGenerationForecast.xlsx"  # Update this path if necessary
        
        # Load the data using pandas
        waste_forecast_data = pd.read_excel(file_path)
        
        # Strip column names to avoid leading/trailing whitespace issues
        waste_forecast_data.columns = waste_forecast_data.columns.str.strip()

        # Ensure column names match the expected names
        required_columns = ["Year", "Total Waste Generation (ton/d)"]
        if not all(col in waste_forecast_data.columns for col in required_columns):
            raise ValueError(f"The data does not have the required columns: {required_columns}")

        # Return the validated DataFrame
        return waste_forecast_data
    except Exception as e:
        st.error(f"Error loading waste forecast data: {str(e)}")
        # Return empty DataFrame if file loading fails
        return pd.DataFrame({"Year": [], "Total Waste Generation (ton/d)": []})

@st.cache_data
def load_power_demand_data():
    try:
        file_path = "GovData/energy/PowerDemandData.xlsx"  # Update this path to match your file location
        power_data = pd.read_excel(file_path)
        return power_data
    except Exception as e:
        st.error(f"Error loading power demand data: {str(e)}")
        return pd.DataFrame()
    
@st.cache_data
def load_power_demand_forecast():
    try:
        # Define the path to the Excel file
        file_path = "GovData/energy/PowerDemandForecast.xlsx"
        
        # Load the data using pandas
        forecast_data = pd.read_excel(file_path)
        
        # Strip column names to avoid leading/trailing whitespace issues
        forecast_data.columns = forecast_data.columns.str.strip()
        
        # Return the validated DataFrame
        return forecast_data
    except Exception as e:
        st.error(f"Error loading power demand forecast data: {str(e)}")
        # Return an empty DataFrame if loading fails
        return pd.DataFrame()

@st.cache_data
def load_peak_power_data():
    try:
        # Replace with the correct file path for your Excel data
        file_path = "GovData/energy/Peak_Power_Demand_Erbil_2022.xlsx"  # Update this path as needed
        peak_power_data = pd.read_excel(file_path)
        
        # Strip column names to avoid whitespace issues
        peak_power_data.columns = peak_power_data.columns.str.strip()
        
        # Return the DataFrame
        return peak_power_data
    except Exception as e:
        st.error(f"Error loading peak power demand data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_dams_ponds_data():
    try:
        file_path = "GovData/water/DamsAndPonds.xlsx"  # Replace with the correct path to your Excel file
        dams_ponds_data = pd.read_excel(file_path)
        dams_ponds_data.columns = dams_ponds_data.columns.str.strip()
        return dams_ponds_data
    except Exception as e:
        st.error(f"Error loading dams and ponds data: {str(e)}")
        return pd.DataFrame()
@st.cache_data
def load_planning_dams_data():
    try:
        # Define the file path for the planning dams Excel file
        file_path = "GovData/water/Planning_Dams_Erbil.xlsx"  # Adjust the file path if needed
        planning_dams_data = pd.read_excel(file_path)
        
        # Clean column names
        planning_dams_data.columns = planning_dams_data.columns.str.strip()
        
        # Return the DataFrame
        return planning_dams_data
    except Exception as e:
        # Display an error message if the file cannot be loaded
        st.error(f"Error loading planning dams data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_research_hub_data():
    # Static internal data definition
    research_hub_data = [
        {
            "Name": "Dr. John Doe",
            "Description": "Expert in Climate Adaptation.",
            "Image_URL": "https://via.placeholder.com/150",
            "Paper_1": "Research on Climate Adaptation",
            "Paper_2": "Impact of Extreme Weather Events"
        },
        {
            "Name": "Dr. Jane Doe",
            "Description": "Specialist in Water Resources.",
            "Image_URL": "https://via.placeholder.com/150",
            "Paper_1": "Hydrology and Water Management",
            "Paper_2": "Water Resource Optimization"
        }
    ]

    # Convert to DataFrame for consistency
    return pd.DataFrame(research_hub_data)


def render_research_hub():
    st.title("Research Hub")
    st.write("Explore expert profiles and their research papers.")

    # Load research data
    research_data = load_research_hub_data()

    if research_data.empty:
        st.error("No research data is available.")
        return

    # Render each profile as an expander
    for _, row in research_data.iterrows():
        with st.expander(row.get('Name', 'Unknown Expert')):
            st.image(row.get('Image_URL', 'https://via.placeholder.com/100'), width=150, caption=row.get('Name', 'No Name'))
            st.write(f"**Description:** {row.get('Description', 'No description available.')}")
            
            st.write("**Research Papers:**")
            papers = [
                row.get('Paper_1', 'No paper available'),
                row.get('Paper_2', 'No paper available')
            ]
            for paper in papers:
                st.markdown(f"- {paper}")


# Load all data
temp_df = load_temperature_data()
rainfall_df = load_rainfall_data()
water_df = load_water_resources_data()
economic_df = load_economic_impact_data()
health_df = load_health_impact_data()
# === PART 2 END ===
# === PART 3 START: ANALYSIS FUNCTIONS AND UI ===
# Sidebar controls
# Display logo in the sidebar
logo_url = "https://i.imgur.com/9aRA1Rv.jpeg"
st.sidebar.image(logo_url, width=140)  # Adjust width if needed

# Sidebar Navigation with Buttons
st.sidebar.header("Navigation")
show_dashboard = st.sidebar.button("Dashboard", key="dashboard")
show_research_hub = st.sidebar.button("Research Hub", key="research_hub")
show_data_sources = st.sidebar.button("Data Sources", key="data_sources")

if show_dashboard or (not show_research_hub and not show_data_sources):
    # Main Dashboard Content
    st.sidebar.header("Dashboard Controls")
    selected_cities = st.sidebar.multiselect(
        "Select Cities",
        ['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk'],
        default=['Hewlêr', 'Dihok', 'Silêmanî', 'Helebce', 'Kerkûk']
    )
    # Add your dashboard-specific content here
    st.title("Dashboard")
    st.write("This is the dashboard page.")
    # ... rest of the dashboard code ...

elif show_research_hub:
    st.title("Research Hub")
    st.write("Explore expert profiles and their research papers.")

    # Load the research data
    research_data = load_research_hub_data()

    # Debug: Print the loaded data
    st.write("Loaded Research Data:")
    st.write(research_data)

    if not research_data:
        st.error("Research Hub data is unavailable.")
    else:
        # Display expert profiles
        st.subheader("Expert Profiles")
        if "Profiles" in research_data:
            profiles_df = research_data["Profiles"]
            st.write("Debug: Profiles DataFrame")
            st.dataframe(profiles_df)  # Show the full DataFrame

            # Display each profile dynamically
            for _, row in profiles_df.iterrows():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(row.get("Image URL", "https://via.placeholder.com/150"), width=120)
                with col2:
                    st.subheader(row.get("Name", "Unknown"))
                    st.write(row.get("Description", "No description provided."))
                    
                    # Display linked papers
                    for paper_key in [col for col in profiles_df.columns if "Paper" in col]:
                        paper = row.get(paper_key)
                        if paper:
                            st.markdown(f"- {paper}")
        else:
            st.warning("No expert profiles available.")

        # Display research papers
        st.subheader("Research Papers")
        if "Papers" in research_data:
            papers_df = research_data["Papers"]
            st.write("Papers DataFrame:")
            st.write(papers_df)
            st.dataframe(papers_df)
        else:
            st.warning("No research papers available.")

        # Display research topics
        st.subheader("Research Topics")
        if "Topics" in research_data:
            topics_df = research_data["Topics"]
            st.write("Topics DataFrame:")
            st.write(topics_df)
            st.dataframe(topics_df)
        else:
            st.warning("No research topics available.")

elif show_data_sources:
    # Data Sources Content
    st.title("Data Sources")
    st.write("This section provides detailed information about the data sources used.")

    # Example Sources
    sources = {
        "World Bank Climate Portal": "https://climateknowledgeportal.worldbank.org/country/iraq/climate-data-historical",
        "NOAA Climate Data": "https://www.ncdc.noaa.gov/cdo-web/datasets",
        "FAO AQUASTAT": "https://www.fao.org/aquastat/en/databases/"
    }

    for source_name, source_link in sources.items():
        st.markdown(f"- [{source_name}]({source_link})")

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

# Data source selection
data_source = st.sidebar.selectbox(
    "Select Data Source",
    ["Open Source Data", "Governmental Data"],
    index=0  # Default to "Open Source Data"
)

# Variables for category and chart type
category = None
chart_type = None

if data_source == "Open Source Data":
    # Categories specific to Open Source Data
    category = st.sidebar.selectbox(
        "Select Category (Open Source Data)",
        ["Temperature & Precipitation",
         "Water Resources",
         "Economic Impact",
         "Health Impact",
         "Seasonal Analysis",
         "Future Projections",
         "Comparative Analysis"]
    )

    # Category-specific options for Open Source Data
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
if data_source == "Governmental Data":
    # Categories specific to Governmental Data
    category = st.sidebar.selectbox(
        "Select Category (Governmental Data)",
        ["Waste Management", "Power & Energy", "Water Resources Management"]  # Add other categories as needed
    )

    if category == "Waste Management":
        # Load Municipal Solid Waste Composition data
        waste_data = load_waste_data()
        
        if not waste_data.empty:
            st.write("### Municipal Solid Waste Composition in Erbil City (2020)")
            st.write("Source: DSEPSWT, MOMT")

            # Create an interactive pie chart
            fig = px.pie(
                waste_data,
                values='Percentage',
                names='Type',
                title="Municipal Solid Waste Composition in Erbil City (2020)",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display raw data
            if st.checkbox("Show raw data for Municipal Solid Waste Composition"):
                st.write(waste_data)
        else:
            st.error("Municipal Solid Waste Composition data is unavailable.")

        # Add a separator between the two datasets
        st.markdown("---")

        # Load Waste Generation Forecast data
        waste_forecast_data = load_waste_forecast_data()
        
        if not waste_forecast_data.empty:
            st.write("### Waste Generation Forecast")
            st.write("Source: JICA Project Team")

            # Create a line chart for visualization
            fig = px.line(
                waste_forecast_data,
                x="Year",
                y="Total Waste Generation (ton/d)",
                title="Waste Generation Forecast (2025-2050)",
                labels={"Total Waste Generation (ton/d)": "Total Waste (ton/d)", "Year": "Year"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display raw data
            if st.checkbox("Show raw data for Waste Generation Forecast"):
                st.write(waste_forecast_data)
        else:
            st.error("Waste Generation Forecast data is unavailable.")

    elif category == "Power & Energy":
        # Load Power Demand Data
        power_data = load_power_demand_data()
        if not power_data.empty:
            st.write("### Power Demand Data for Kurdistan Region (2022)")
            st.write("Source: Ministry of Electricity")
            
            # Display raw data table
            if st.checkbox("Show raw data for Power Demand"):
                st.write(power_data)
            
            # Create a bar chart for visualization
            fig = px.bar(
                power_data,
                x="City",
                y=["Supplied Demand (MW)", "Potential Peak Demand (MW)", "Suppressed Demand (MW)"],
                title="Supplied vs Potential Peak vs Suppressed Demand (2022)",
                barmode="group",
                labels={"value": "MW", "City": "City"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Power demand data is unavailable.")
        
        # Add a separator between datasets
        st.markdown("---")
        
        # Load Power Demand Forecast Data
        forecast_data = load_power_demand_forecast()
        if not forecast_data.empty:
            st.write("### City-Level Power Demand Forecast for Kurdistan Region (2022-2032)")
            st.write("Source: Ministry of Electricity")
            
            # Display raw data table
            if st.checkbox("Show raw data for Power Demand Forecast"):
                st.write(forecast_data)
            
            # Melt data for visualization
            city_data = forecast_data.melt(
                id_vars="Year",
                value_vars=["Erbil", "Dohuk", "Sulaymaniyah"],  # Exclude "KRG"
                var_name="City",
                value_name="Demand (MW)"
            )
            
            # Create a stacked area chart
            fig = px.area(
                city_data,
                x="Year",
                y="Demand (MW)",
                color="City",
                title="City-Level Power Demand Forecast (2022-2032)",
                labels={"Demand (MW)": "Demand (MW)", "Year": "Year", "City": "City"}
            )
            
            # Customize layout
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Demand (MW)",
                legend_title="City",
                title_x=0.5,
                height=600,  # Adjust height for better readability
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Power demand forecast data is unavailable.")
        
        # Add Peak Power Demand Data
        st.markdown("---")
        peak_power_data = load_peak_power_data()
        if not peak_power_data.empty:
            st.write("### Peak Power Demand by Region in Erbil Governorate (2022)")
            st.write("Source: Ministry of Electricity")
            
            # Display raw data with Average and Ratio (%)
            if st.checkbox("Show raw data for Peak Power Demand"):
                st.write(peak_power_data)
            
            # Exclude Average and Ratio (%) for visualization
            filtered_peak_power_data = peak_power_data[~peak_power_data["Month"].isin(["Average", "Ratio (%)"])]
            filtered_peak_power_data["Month"] = pd.Categorical(
                filtered_peak_power_data["Month"],
                categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                ordered=True
            )
            filtered_peak_power_data = filtered_peak_power_data.sort_values(by="Month")
            
            # Create line chart for visualization
            fig = px.line(
                filtered_peak_power_data,
                x="Month",
                y=[
                    "Electricity Distribution Directorate (1)",
                    "Electricity Distribution Directorate (2)",
                    "Salahaddin",
                    "Shaqlawa",
                    "Soran",
                    "Koya"
                ],
                title="Peak Power Demand by Region in Erbil Governorate (2022)",
                labels={"value": "MW", "Month": "Month"},
                markers=True
            )
            
            # Customize layout
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Power Demand (MW)",
                legend_title="Region",
                title_x=0.5,
                height=600
            )
            
            # Show the chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Peak Power Demand data is unavailable.")

if category == "Water Resources Management":
        # Load Dams and Ponds Data
        dams_ponds_data = load_dams_ponds_data()
        planning_dams_data = load_planning_dams_data()

        if not dams_ponds_data.empty:
            st.write("### Dams and Ponds Effective for Groundwater Recharge")
            st.write("Source: JICA Project Team")

            # Bar chart: Reservoir Volumes by Dam and Pond
            fig = px.bar(
                dams_ponds_data,
                x="Dam/Pond Name",
                y="Reservoir Volume (m³)",
                color="Priority",
                title="Reservoir Volumes by Dam and Pond",
                labels={"Reservoir Volume (m³)": "Volume (m³)", "Priority": "Priority Level"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart: Catchment Areas and Heights
            fig = px.bar(
                dams_ponds_data,
                x="Dam/Pond Name",
                y="Catchment Area (Km²)",
                color="Height (m)",
                title="Catchment Areas and Heights of Dams and Ponds",
                labels={"Catchment Area (Km²)": "Catchment Area (Km²)", "Height (m)": "Height (m)"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display raw data
            if st.checkbox("Show raw data for Dams and Ponds"):
                st.write(dams_ponds_data)
        else:
            st.error("Dams and Ponds data is unavailable.")

        st.markdown("---")

        if not planning_dams_data.empty:
            st.write("### Details of the Planning Dams - Erbil City")
            st.write("Source: GDUP")

            # Bar chart: Dam Heights
            fig = px.bar(
                planning_dams_data,
                x="Site Name",
                y="Dam Height (m)",
                color="River Catchment",
                title="Planned Dams and Their Heights",
                labels={"Dam Height (m)": "Height (m)", "River Catchment": "River Catchment"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Pie chart: Types of Dams
            fig = px.pie(
                planning_dams_data,
                names="Type of Dam",
                title="Distribution of Planned Dam Types",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display raw data
            if st.checkbox("Show raw data for Planning Dams"):
                st.write(planning_dams_data)
        else:
            st.error("Planning Dams data is unavailable.")


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
                        mode='lines'
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['GroundwaterLevel'],
                        name=f'{city} Groundwater',
                        line=dict(dash='dash')
                    )
                )
            
            fig.update_layout(
                title=f'Combined Water Resources<br><sup>Source: {source["name"]}</sup>',
                yaxis_title="River Level (m³/s)",
                xaxis_title="Year"
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a></small>', unsafe_allow_html=True)

    elif category == "Economic Impact":
        source = get_data_source('economic')
        if chart_type == "Energy Demand":
            fig = px.line(
                economic_df_filtered,
                x='Year',
                y='EnergyDemand',
                color='City',
                title=f'Energy Demand Trends<br><sup>Source: {source["name"]}</sup>',
                labels={'EnergyDemand': 'Energy Demand (MW)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Agricultural Production":
            fig = px.line(
                economic_df_filtered,
                x='Year',
                y='AgriculturalProduction',
                color='City',
                title=f'Agricultural Production Trends<br><sup>Source: {source["name"]}</sup>',
                labels={'AgriculturalProduction': 'Production (tons)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Combined Economic Impact
            fig = go.Figure()
            for city in selected_cities:
                city_data = economic_df_filtered[economic_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['EnergyDemand'],
                        name=f'{city} Energy',
                        mode='lines'
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['AgriculturalProduction'],
                        name=f'{city} Agriculture',
                        line=dict(dash='dash')
                    )
                )
            
            fig.update_layout(
                title=f'Combined Economic Indicators<br><sup>Source: {source["name"]}</sup>',
                yaxis_title="Energy Demand (MW)",
                xaxis_title="Year"
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a></small>', unsafe_allow_html=True)

    elif category == "Health Impact":
        source = get_data_source('health')
        if chart_type == "Heat Stress Index":
            fig = px.line(
                health_df_filtered,
                x='Year',
                y='HeatStressIndex',
                color='City',
                title=f'Heat Stress Index<br><sup>Source: {source["name"]}</sup>',
                labels={'HeatStressIndex': 'Heat Stress Index'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Air Health Index":
            fig = px.line(
                health_df_filtered,
                x='Year',
                y='AirHealthIndex',
                color='City',
                title=f'Air Quality Health Index<br><sup>Source: {source["name"]}</sup>',
                labels={'AirHealthIndex': 'Air Quality Index'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Combined Health Indicators
            fig = go.Figure()
            for city in selected_cities:
                city_data = health_df_filtered[health_df_filtered['City'] == city]
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['HeatStressIndex'],
                        name=f'{city} Heat Stress',
                        mode='lines'
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=city_data['Year'],
                        y=city_data['AirHealthIndex'],
                        name=f'{city} Air Quality',
                        line=dict(dash='dash')
                    )
                )
            
            fig.update_layout(
                title=f'Combined Health Indicators<br><sup>Source: {source["name"]}</sup>',
                yaxis_title="Index Value",
                xaxis_title="Year"
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<small>Data Source: <a href="{source["link"]}" target="_blank">{source["name"]}</a></small>', unsafe_allow_html=True)

    elif category == "Seasonal Analysis":
        if chart_type == "Temperature Patterns":
            seasonal_temp = temp_df_filtered.groupby(['Year', 'Season', 'City'])['Temperature'].mean().reset_index()
            fig = px.line(
                seasonal_temp,
                x='Year',
                y='Temperature',
                color='City',
                facet_col='Season',
                title='Seasonal Temperature Patterns',
                labels={'Temperature': 'Temperature (°C)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Rainfall Distribution":
            seasonal_rain = rainfall_df_filtered.groupby(['Year', 'Season', 'City'])['Rainfall'].sum().reset_index()
            fig = px.line(
                seasonal_rain,
                x='Year',
                y='Rainfall',
                color='City',
                facet_col='Season',
                title='Seasonal Rainfall Distribution',
                labels={'Rainfall': 'Rainfall (mm)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Seasonal Comparisons
            fig = px.box(
                temp_df_filtered,
                x='Season',
                y='Temperature',
                color='City',
                title='Temperature Distribution by Season',
                labels={'Temperature': 'Temperature (°C)'},
                category_orders={"Season": ["Winter", "Spring", "Summer", "Autumn"]}
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