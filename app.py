from crew import VacationPlanner
import streamlit as st
from streamlit_folium import folium_static
from helper import Helper

st.title("Vacation Planning Assistant")
destination = st.sidebar.text_input("Destination", placeholder="Enter destination")
starting_point = st.sidebar.text_input("Starting Point", placeholder="Enter current location")
preferences = st.sidebar.text_area("Preferences", placeholder="Museums, Food, Beaches, etc.")

if st.sidebar.button("Generate Itinerary"):
    if not starting_point or not destination or not preferences:
        st.error("All inputs are required: Starting Point, Destination, and Preferences.")
    else:
        inputs = {
            "starting_point": starting_point,
            "destination": destination,
            "preferences": preferences
        }

        result = VacationPlanner().crew().kickoff(inputs=inputs)
        st.markdown(result)

        # Generate Map
        m = Helper.geocode(result, destination, starting_point)
        folium_static(m, width=700, height=500)
