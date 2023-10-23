# App for creating the schedule for the matches between individuals for the Wayside Athletic Club Racquetball League
##########Backlog Items##############
# 1. Check for other availability files and ask user if they should be included in the schedule

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
def makeSchedule(seas, nm, abw, sd, yr, np, pl, rs):

    #### sub-function to choose the teams with the least amount of byes
    def byePlayerFunc(playerstoChooseFrom=[]):
        if len(playerstoChooseFrom) == 0:
            playerswMinByeGames = playerTrack[playerTrack['byeCount'] == min(playerTrack['byeCount'])].player
            if debugInd == 1: st.write("playerswMinByeGames (in if) = ", playerswMinByeGames)
        else:
            teamswMinByeGames = playerstoChooseFrom
            if debugInd == 1: st.write("playerswMinByeGames (in else) = ", playerswMinByeGames)
        if (np % 2 == 1):
            byePl = pd.DataFrame(playerswMinByeGames, columns=['player']).sample(n=1, random_state=rs).squeeze(axis=1)
        else:
            byePl = ""
        return byePl

    #### End byeTeamFunc function

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
    byeWeekCnt = math.ceil(schedMatches/(abw + 1))

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

    if debugInd == 1: st.write("startDay =", startDay)

    #### Go through assigning matches from the first day chronologically to the last
    gameDay = startDay
    byeCounter = 1

    for i in range(1, schedMatches, 1):
        startIndex = (matchesPerWeek * (i - 1)) + 1
        endIndex = matchesPerWeek * i
        if debugInd == 1: st.write("gameday =", gameDay)
        ##### Before assigning the matches, make sure the date is correct
        for j in range(startIndex, endIndex + 1):
            leagueSched.loc[j - 1, 'date'] = gameDay
        ##### First, select the player to have a bye, users can not adjust this preference
        if byeCounter == byeWeekCnt:
            ###### If this is a bye week for all players, assign all players to the list of byes and reset the counter
            byePlayers = list(players)
            byeCounter = 1
        else:
            byePlayers = byePlayerFunc()
            byeCounter = byeCounter + 1
        ##### Second, let's make sure home games are evened out as much as possible when choosing home teams this week
        else:
            if (totalTeams % 2 == 1):
                teamswMinHomeGames = homeGameFunc(teamTrack[teamTrack['team'] != byePlayers.values[0]].team, 'min')
                firstChoiceTeams = set([x for x in teamList if x not in byeTeams.values]).intersection(
                    teamswMinHomeGames.values)
                if debugInd == 1: st.write("firstChoiceTeams = ", firstChoiceTeams)
            else:
                teamswMinHomeGames = homeGameFunc(teamTrack['team'], 'min')
                firstChoiceTeams = [x for x in teamList if x in teamswMinHomeGames.values]
                if debugInd == 1: st.write("firstChoiceTeams = ", firstChoiceTeams)
        if (len(firstChoiceTeams) < gamesPerGameDay):
            if debugInd == 1: st.write("inside firstChoiceTeams if, need more home teams")
            ##### find how many more home teams need to be chosen for this date
            homeGameDiff = gamesPerGameDay - len(firstChoiceTeams)
            ##### Third, choose from among the remaining teams, those who have not played the most home games
            teamswMaxHomeGames = homeGameFunc(teamTrack['team'], 'max')
            if (totalTeams % 2 == 1):
                sct = set([y for y in teamList if y not in byeTeams.values])
                sct2 = set([y2 for y2 in sct if y2 not in firstChoiceTeams])
            else:
                sct2 = set([y2 for y2 in teamList if y2 not in firstChoiceTeams])
            secondChoiceTeams = set([y3 for y3 in sct2 if y3 not in teamswMaxHomeGames])
            if debugInd == 1: st.write("secondChoiceTeams = ", secondChoiceTeams)
            if (len(secondChoiceTeams) < homeGameDiff):
                if debugInd == 1: st.write("inside secondChoiceTeams if, still don't have enough home teams")
                ##### find how many more home teams need to be chosen for this date
                homeGameDiff2 = gamesPerGameDay - len(firstChoiceTeams) - len(secondChoiceTeams)
                ##### Last, choose randomly from among the remaining teams
                if (totalTeams % 2 == 1):
                    tct = set([y for y in teamList if y not in byeTeams.values])
                    tct2 = set([y2 for y2 in tct if y2 not in firstChoiceTeams])
                else:
                    tct2 = set([y2 for y2 in teamList if y2 not in firstChoiceTeams])
                thirdChoiceTeams = set([y3 for y3 in tct2 if y3 not in secondChoiceTeams])
                tiTemp = set(
                    pd.DataFrame(thirdChoiceTeams).sample(n=homeGameDiff2, random_state=rs, replace=False).squeeze(
                        axis=1))
                tiTemp2 = tiTemp.union(secondChoiceTeams)
                teamsIncluded = pd.DataFrame(tiTemp2.union(firstChoiceTeams))
            else:
                if debugInd == 1: st.write("inside secondChoiceTeams else, found enough home teams")
                tiTemp = set(
                    pd.DataFrame(secondChoiceTeams).sample(n=homeGameDiff, random_state=rs, replace=False).squeeze(
                        axis=1))
                teamsIncluded = pd.DataFrame(tiTemp.union(firstChoiceTeams))
        else:
            teamsIncluded = pd.DataFrame(firstChoiceTeams).sample(n=gamesPerGameDay, random_state=rs, replace=False)
        homeTeams = teamsIncluded
        ##### Now, choose opponents, try and avoid duplicate matches and inter-town matches if possible
        if (totalTeams % 2 == 1):
            awt = set([z for z in teamList if z not in byeTeams.values])
            awayTeams = set([z2 for z2 in awt if z2 not in set(homeTeams.squeeze(axis=1))])
            if debugInd == 1: st.write("awayTeams = ", awayTeams)
        else:
            awayTeams = set([z for z in list(teamList) if z not in set(homeTeams.squeeze(axis=1))])
            if debugInd == 1: st.write("awayTeams = ", awayTeams)
        ##### Convert the home teams and away teams sets into lists so we can subset them
        homeTeams = homeTeams[0].tolist()
        awayTeams = list(awayTeams)
        endFlag1 = 1
        for i2 in range(0, len(homeTeams)):
            if debugInd == 1: st.write("i2 = ", i2)
            if debugInd == 1: st.write("awayTeams[i2] = ", awayTeams[i2])
            if debugInd == 1: st.write("homeTeams[i2] = ", homeTeams[i2])
            ptstr = teamTrack.loc[teamTrack['team'] == homeTeams[i2], 'playedTeams']
            with pd.option_context('display.max_colwidth', -1):
                ps = ptstr.to_string()
            if debugInd == 1: st.write("str(ps) = ", ps)
            if awayTeams[i2] in ps:
                dupTeam = 1
                if debugInd == 1: st.write("in dupTeam assignment")
            else:
                dupTeam = 0
            if re.sub('[^A-Za-z]+', '', awayTeams[i2]) == re.sub('[^A-Za-z]+', '', homeTeams[i2]):
                sameTown = 1
                if debugInd == 1: st.write("in sameTown assignment")
            else:
                sameTown = 0
            if dupTeam == 1 or sameTown == 1:
                endFlag1 = 0
            if i2 < len(awayTeams) and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(i2 + 1, len(awayTeams), i2, 1, 1)
                if debugInd == 1: st.write("After first dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
            ###### If we've gotten to the end and there is a still a duplicate match, check back at the beginning
            if i2 > 0 and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(0, i2, i2, 1, 1)
                if debugInd == 1: st.write("After second dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
            ###### If we can't get matchups avoiding duplicates and same town matchups, at least avoid duplicates
            if i2 < len(awayTeams) and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(i2 + 1, len(awayTeams), i2, 1, 0)
                if debugInd == 1: st.write("After third dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
            ###### If we've gotten to the end and there is a still a duplicate match, check back at the beginning
            if i2 > 0 and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(0, i2, i2, 1, 0)
                if debugInd == 1: st.write("After fourth dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
            ###### If we still can't avoid duplicates, at least try and avoid match-ups between teams in the same town as a last resort
            if i2 < len(awayTeams) and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(i2 + 1, len(awayTeams), i2, 0, 1)
                if debugInd == 1: st.write("After fifth dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
            ###### If we've gotten to the end and there is a still a same town match-up, check back at the beginning
            if i2 > 0 and endFlag1 == 0:
                endFlag1 = dupSameTownCheckFunc(0, i2, i2, 0, 1)
                if debugInd == 1: st.write("After sixth dupSameTownCheckFunc call and endFlag1 = ", endFlag1)
        teamIndex = 0
        for l in range(startIndex - 1, endIndex):
            leagueSched.loc[l, 'homeTeam'] = homeTeams[teamIndex]
            leagueSched.loc[l, 'awayTeam'] = ""
            if (twnm == 'Have Inter-Town Match-Ups to End the Season (if possible)' and i == schedGames):
                for m in range(0, len(sameTownTeamsHome)):
                    if homeTeams[teamIndex] == sameTownTeamsHome[m]:
                        leagueSched.loc[l, 'awayTeam'] = sameTownTeamsAway[m]
                if leagueSched.loc[l, 'awayTeam'] == "":
                    if (totalTeams % 2 == 1):
                        lat = set([v for v in teamList if v not in byeTeams.values])
                        lat2 = set([v for v in lat if v not in sameTownTeamsAway])
                        lastAwayTemp = list(set([v2 for v2 in lat2 if v2 not in homeTeams]))[0]
                        if debugInd == 1: st.write("lastAwayTemp = ", lastAwayTemp)
                    else:
                        lat = set([v for v in teamList if v not in homeTeams])
                        lastAwayTemp = list(set([v2 for v2 in lat if v2 not in sameTownTeamsAway]))[0]
                        if debugInd == 1: st.write("lastAwayTemp = ", lastAwayTemp)
                    leagueSched.loc[l, 'awayTeam'] = lastAwayTemp
            else:
                leagueSched.loc[l, 'awayTeam'] = awayTeams[teamIndex]
            teamIndex += 1
        # Should only be 1 player with a bye or the whole group
        if (np % 2 == 1):
            playerTrack.loc[playerTrack['player'] == byePlayers.values[0], 'byeCount'] += 1
        for j in range(0, len(playerOnes)):
            playerTrack.loc[playerTrack['player'] == playerOnes[j], 'games'] += 1
            playerTrack.loc[playerTrack['player'] == playerOnes[j], 'playedPlayers'] = playerTrack.loc[playerTrack['player'] == playerOnes[j], 'playedPlayers'] + ", " + playerTrack[playerTrack['player'] == playerTwos[j]]['player'].values[0]
        for k in range(0, len(playerTwos)):
            playerTrack.loc[playerTrack['team'] == playerTwos[k], 'awayGames'] += 1
            playerTrack.loc[playerTrack['team'] == playerTwos[k], 'playedPlayers'] = playerTrack.loc[playerTrack['player'] == playerTwos[k], 'playedPlayers'] + ", " + playerTrack[playerTrack['team'] == playerOnes[k]]['team'].values[0]

        if gameDay.weekday() in range(0, 2):
            if ((gameDay - dt.timedelta(days=5)) in us_holidays):
                gameDay = gameDay - dt.timedelta(days=7)
            else:
                gameDay = gameDay - dt.timedelta(days=5)
        elif gameDay.weekday() in range(2, 4):
            if ((gameDay - dt.timedelta(days=2)) in us_holidays):
                gameDay = gameDay - dt.timedelta(days=7)
            else:
                gameDay = gameDay - dt.timedelta(days=2)
        ##### For weekend games, we need an added check to see if the previous Monday is a holiday, making it a holiday weekend
        elif gameDay.weekday() in range(5, 7):
            if ((gameDay - dt.timedelta(days=7)) in us_holidays or (gameDay - dt.timedelta(days=6)) in us_holidays or (
                    gameDay - dt.timedelta(days=5)) in us_holidays):
                gameDay = gameDay - dt.timedelta(days=14)
            else:
                gameDay = gameDay - dt.timedelta(days=7)

        ##### Check that byes are even
        if (max(playerTrack['byeCount']) >= (min(playerTrack['byeCount']) + 2)):
            st.error("Error: Byes are Not Being Evenly Distributed")
        rs += 1
    #### End for loop
    blankIndex = [''] * len(playerTrack)
    playerTrack = playerTrack.rename(
        columns={"team": "Team", "games": "Matches", "byeCount": "Bye Count",
                 "playedPlayers": "Played Players"})
    playerTrack.index = blankIndex
    leagueSched = leagueSched.rename(columns={"date": "Date", "player1": "Player 1", "player2": "Player 2"})
    st.header(leag + " Player Tracking Summary for " + seas + " Season")
    st.table(playerTrack.style)
    st.header(yr + " Schedule for " + seas + " Season")
    st.table(leagueSched.sort_index())

# End makeSchedule function

# Sidebar Design
st.sidebar.header("Schedule Inputs")
### Pick the season
season = st.sidebar.radio('Select the Season', ['Fall', 'Winter', 'Spring'])
### Select the number of <atches>
numberMatches = st.sidebar.number_input("Enter the Number of Matches to Be Played", value=12, min_value=1)
### Option to automatically include a bye week for all players (helps ensure all games are played)
autoByeWeek = st.sidebar.number_input("Enter the Number of Bye Weeks to Include in the Schedule (if any) ", value=0, min_value=0)
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
    makeSchedule(season, numberMatches, autoByeWeek, startDay, year, numPlayers, players, randomSeed)
