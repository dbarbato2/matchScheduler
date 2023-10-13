# App for creating the schedule for the matches between individuals for the Wayside Athletic Club Racquetball League
##########Backlog Items##############

import streamlit as st
import pandas as pd
import holidays
import random

# Create a Streamlit web app
st.title("Racquetball Scheduling")
us_holidays = holidays.UnitedStates()
### Indicator on whether to run the app in debug mode (makes the schedule calculation repeatable)
debugInd = 0

# Upload a CSV file containing user availability
uploaded_file = st.file_uploader("Upload a CSV file with user availability", type=["csv"])

# Function for creating the schedule
def makeSchedule(seas, nm, sd, yr, np, rs):
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        availability_df = pd.read_csv(uploaded_file)

        # Display user availability
        st.write("User Availability:")
        st.table(availability_df)

        # Function to schedule matches
        def schedule_matches(availability_df, num_matches):
            availability_slots = availability_df['Availability'].tolist()
            if len(availability_slots) < num_matches:
                return "Not enough availability for the specified number of matches."

            random.shuffle(availability_slots)
            return availability_slots[:num_matches]

        # Get the number of matches to schedule
        num_matches = st.number_input("Number of Matches to Schedule", min_value=1, step=1, value=1)

        # Schedule matches
        scheduled_matches = schedule_matches(availability_df, num_matches)

        # Display the scheduled matches
        st.write(f"Scheduled Matches ({num_matches} out of {len(availability_df)} available):")
        scheduled_matches_df = pd.DataFrame({"Match": [f"Match {i + 1}" for i in range(num_matches)],
                                             "Time Slot": scheduled_matches})
        st.table(scheduled_matches_df)

# End makeSchedule function

# Sidebar Design
st.sidebar.header("Schedule Inputs")
### Pick the season
season = st.sidebar.radio('Select the Season', ['Fall', 'Winter', 'Spring'])
### Select the number of Games
numberMatches = st.sidebar.number_input("Enter the Number of Matches to Be Played", value=12)
### Determine if the start date should be calculated
sdCalc = st.sidebar.checkbox("Manually enter the league start date?")
if sdCalc:
    startDay = st.sidebar.date_input("League Start Date (first set of matches)")
else:
    startDay = ""
### Enter the year
year = st.sidebar.number_input("Enter the Year", 2020, 2100, 2023)
### Set the total number of Players for the for loop
numPlayers = st.sidebar.number_input("How many people are playing?", 1, 50)
### Enter the towns and the number of teams within each town
players = []
players.append(st.sidebar.text_input("Enter the first player to add to the schedule", ""))
if numPlayers > 1:
    for x in range(1, numPlayers):
        players.append(st.sidebar.text_input(f'Enter the number {x + 1:2d} player name', ""))

schedButton = st.button("Calculate Schedule")
### Random seed for choosing teams, this should be different each time the button is pressed so a new schedule is generated
if debugInd == 1:
    randomSeed = 10
else:
    randomSeed = random.randint(1, 100)

# Main Panel Design
if schedButton:
    makeSchedule(season, numberMatches, startDay, year, numPlayers, randomSeed)
