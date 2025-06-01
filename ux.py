# import all------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import import_ipynb
import datacleaning as dc
import matplotlib.pyplot as plt
# Load data--------------------------------------------------------------------------
dc1=dc.mergedf()
df= dc1.add()
st.set_page_config(page_title="Bird Data Dashboard", layout="wide")
st.title(":bird: Bird Monitoring Dashboard")
#-----------------------------------------------------------------------------------------------------------
#sidebar navigator
st.sidebar.header("Navigation :bird:")
page = st.sidebar.radio("Go to", [
    ":house: Homepage Dashboard",
    " 🌍 Location Insights",
    "🧑‍🔬 Observer Reports",
    "🐦 Bird Species Profile",
    " 📊 Plot insights",
    "☠️ At Risk",
    "📅 Date filter",
    ":cloud: Whether Analyze",
    "📈 Behavior Patterns"

])
#home -----------------------------------------------------------------------------------------------------------
if page==":house: Homepage Dashboard":
    st.title(":house: Homepage Dashboard")
    st.write("""Reads and consolidates multiple Excel sheets into a unified dataset.

Provides interactive filters to select specific observers and locations.

Displays key metrics such as unique bird species counts.

Visualizes behavioral data with dynamic scatter plots categorized by bird sex.

Handles data cleaning with warnings suppression and proper dataframe operations.""")
    
    st.header("📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(df))
    col2.metric("Unique Species", df['Common_Name'].nunique())
    col3.metric("Observers", df['Observer'].nunique())
    col4.metric("Sites", df['Site_Name'].nunique())

#----------------------------------------------------------------------------------------------------------------------

# 🌍 Location Insights
if page ==" 🌍 Location Insights":
    st.header(" 🌍 Location Insights")
    site_plot = df.groupby(['Site_Name', 'Plot_Name']).size().reset_index(name='Count')
    fig_site = px.bar(site_plot, x="Site_Name", y="Count", color="Plot_Name", title="Sightings by Site and Plot")
    st.plotly_chart(fig_site, use_container_width=True)
#------------------------------------------------------------------------------------------------------------------------------
# 🧑‍🔬 Observer Reports
if page =="🧑‍🔬 Observer Reports":
    st.header("🧑‍🔬 Observer Reports")
    selected_observer = st.selectbox("Choose an Observer", df['Observer'].dropna().unique())
    observer_df = df[df['Observer'] == selected_observer]
    selected_Location = st.selectbox("Choose a Location", df['Location_Type'].dropna().unique())
    observer_df = df[(df['Observer'] == selected_observer) & (df['Location_Type'] == selected_Location)]
    st.write(observer_df[['Date', 'Common_Name',"Scientific_Name", 'Initial_Three_Min_Cnt']])
#------------------------------------------------------------------------------------------------------------------------------
# 🐦 Species Details
if page == "🐦 Bird Species Profile":
    st.header("🐦 Bird Species Profile")
    selected_species = st.selectbox("Select Bird", df['Common_Name'].dropna().unique())
    species_df = df[df['Common_Name'] == selected_species]
    col1, col2 = st.columns(2)
    fig1 = px.histogram(species_df, x='Sex', title="Sex Distribution")
    fig2 = px.box(species_df, x='Flyover_Observed', y='Distance', title="Flyover vs Distance")
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)
#-----------------------------------------------------------------------------------------------------------------------------
#☠️ At Risk
if page =="☠️ At Risk":
    st.header("☠️ At Risk")
    Risk= df[(df['PIF_Watchlist_Status'] == True) | (df['Regional_Stewardship_Status'] == True)]
    st.write(Risk[['Common_Name',"Scientific_Name", "PIF_Watchlist_Status", "Regional_Stewardship_Status", "Sex"]])
#----------------------------------------------------------------------------------------------------------------------------------
#Whether Analyze
if page==":cloud: Whether Analyze":
    st.header(":cloud: Whether Analysis")
    temp = st.selectbox("Select Temperature", df['Temperature'].dropna().unique())
    humidity = st.selectbox("Select Humidity", df['Humidity'].dropna().unique())
    temp_df = df[(df['Temperature'] == temp)&(df['Humidity'] == humidity)]
    st.subheader("🔍 Birds Found (Temperature & Humidity)")
    st.write(temp_df[['Common_Name',"Scientific_Name"]])
    if not temp_df.empty:
        st.bar_chart(temp_df['Common_Name'].value_counts())
    sky = st.selectbox("Select Sky", df['Sky'].dropna().unique())
    wind = st.selectbox("Select Wind", df['Wind'].dropna().unique())
    sky_df = df[(df['Sky'] == sky)&(df['Wind'] == wind)]
    st.subheader("🔍 Birds Found (Sky & Wind)")
    st.write(sky_df[['Common_Name',"Scientific_Name"]])
    if not sky_df.empty:
        st.bar_chart(sky_df['Common_Name'].value_counts())
    disturbance = st.selectbox("Select Disturbance", df['Disturbance'].dropna().unique())
    disturb_df = df[df['Disturbance'] == disturbance]
    st.subheader("🔍 Birds Found (Disturbance)")
    st.write(sky_df[['Common_Name',"Scientific_Name"]])
    if not disturb_df.empty:
        st.bar_chart(disturb_df['Common_Name'].value_counts())
#---------------------------------------------------------------------------------------------------------------------------------
#📈 Behavior Patterns
if page=="📈 Behavior Patterns":
    st.header("📈 Behavior Patterns")
    st.header("🦅 ID Method vs Flyover Observations")
    if "ID_Method" in df.columns and "Flyover_Observed" in df.columns:
        grouped = df.groupby(["ID_Method", "Flyover_Observed"]).size().unstack(fill_value=0)

        st.subheader("📊 Flyover Observed Count by ID Method")
        st.dataframe(grouped)

    # Bar chart
        st.subheader("📈 Bar Chart: Flyover Observed by ID Method")
        fig, ax = plt.subplots()
        grouped.plot(kind='bar',  stacked=True, ax=ax )
        ax.set_ylabel("Count")
        ax.set_title("Flyover Observed per ID Method")
        st.pyplot(fig)

    else:
        st.error("⚠️ Columns 'ID_Method' or 'Flyover_Observed' not found in your dataset.")
#------------------------------------------------------------------------------------------------------------------------------
#📊 Plot insights
if page==" 📊 Plot insights":
    st.header("📊 Plot insights")
    if "Admin_Unit_Code" in df.columns: 
        lt = df["Admin_Unit_Code"].value_counts()

        # Show counts as a table
        st.subheader("📋 Admin_Unit_Code Type Count")
        st.dataframe(lt)
        st.subheader("📊 Bar Chart: Location Types")
        fig, ax = plt.subplots()
        lt.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_xlabel("Admin_Unit_Code Type")
        ax.set_ylabel("Count")
        ax.set_title("Distribution of Admin_Unit_Code Types")
        st.pyplot(fig)

    else:
        st.error("⚠️ 'Admin_Unit_Code' column not found in your dataset.")
#-----------------------------------------------------------------------------------------------------------------------------------
#📅 Date filter
if page =="📅 Date filter":
    st.header("📅 Date filter")
    selected_date = st.selectbox("Choose a Date", df['Date'].dropna().unique())
    observer_df = df[df['Date'] == selected_observer]
    st.write(observer_df[['Observer', 'Common_Name',"Scientific_Name"]])

