# App for creating the schedule for the matches between individuals for the Wayside Athletic Club Racquetball League
##########Backlog Items##############

import streamlit as st
import pandas as pd
import datetime as dt
import math
import holidays
import random

# Create a Streamlit web app
st.title("Racquetball Scheduling")
us_holidays = holidays.UnitedStates()
### Indicator on whether to run the app in debug mode (makes the schedule calculation repeatable)
debugInd = 0

# Function to load the user availability files for each player
def loadAvailability(nu, pl):
    plFile = pd.DataFrame()
    for y in range(1, nu):
        plShort = pl.replace(' ', '_')
        plFile = pd.read_csv("~/Documents/Python Programs/matchScheduler/userData/" +plShort + "_availability.csv")


# End loadAvailability function

# Function for creating the schedule
def makeSchedule(seas, nm, sd, yr, np, pl, rs):

    ## First, check to see if each player has listed availability and load all of the availability files
    loadAvailability(np, pl)

    #### Second, calculate the start day if it wasn't entered
    if sd == "":
        if seas == "Fall":
            ##### Season starts on the second Monday in September
            firstDay = dt.date(yr, 9, 1)
            wd = firstDay.weekday()
            firstMonday = firstDay + dt.timedelta(days=((7 - wd) % 7))
            startDay = firstMonday + dt.timedelta(days=7)
        if seas == "Winter":
            ##### Season starts on the First Monday in January After New Years
            firstDay = dt.date(yr, 1, 1)
            wd = firstDay.weekday()
            firstMonday = firstDay + dt.timedelta(days=((7 - wd) % 7))
            if (firstMonday) in us_holidays:
                startDay = firstMonday + dt.timedelta(days=7)
            else:
                startDay = firstMonday
        if seas == "Spring":
            ##### Season starts on the first Monday in April
            firstDay = dt.date(yr, 4, 1)
            wd = firstDay.weekday()
            firstMonday = firstDay + dt.timedelta(days=((7 - wd) % 7))
            startDay = firstMonday
    else:
        startDay = sd
    matchesPerWeek = math.floor(np / 2)
    #### If there's an odd number of players, multiple weeks are needed to get to the desired number of matches for each player
    if (np % 2 == 1):
        schedMatches = nm + math.ceil(nm / pl)
    else:
        schedMatches = nm

    #### The schedOutput dataframe tracks the schedule and returns it
    column_names = ["date", "player1", "player2"]
    leagueSched = pd.DataFrame(columns=column_names)
    column_names2 = ["player", "games", "byeCount", "playedPlayers"]
    playerTrack = pd.DataFrame(columns=column_names2)
    for j in range(0, np):
        playerTrack.loc[j, 'player'] = pl[j]
        playerTrack.loc[j, 'games'] = 0
        playerTrack.loc[j, 'byeCount'] = 0
        playerTrack.loc[j, 'playedPlayers'] = ""

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
### Select the number of <atches>
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
### Enter the players names now
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
    makeSchedule(season, numberMatches, startDay, year, numPlayers, players, randomSeed)
