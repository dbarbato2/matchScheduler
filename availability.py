#Backlog items:
# 1.Allow for open and close times to vary by day of the week
# 2.Save the use availability files to a central location, i.e. S3 or Google Drive

import streamlit as st
import pandas as pd

# Create a Streamlit web app
st. set_page_config(layout="wide")
st.title("Availability Scheduler")

# Create a form to collect user availability data
playerName = st.text_area("Enter your name", height=1, max_chars=30)
st.write("Check which times you are available for each day of the week:")

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                'Sunday']  # Define the start and end times
colMonday, colTuesday, colWednesday, colThursday, colFriday, colSaturday, colSunday = st.columns(7)

openTime = 8  # 8 AM
closeTime = 21  # 9 PM

availability_data = pd.DataFrame(columns=['day'])
dayTracker = 1
for day in days_of_week:
    if day == "Monday":
        with colMonday:
            st.subheader("Monday")
    elif day == "Tuesday":
        with colTuesday:
            st.subheader("Tuesday")
    elif day == "Wednesday":
        with colWednesday:
            st.subheader("Wednesday")
    elif day == "Thursday":
        with colThursday:
            st.subheader("Thursday")
    elif day == "Friday":
        with colFriday:
            st.subheader("Friday")
    elif day == "Saturday":
        with colSaturday:
            st.subheader("Saturday")
    else:
        with colSunday:
            st.subheader("Sunday")
    #st.write("dayTracker = ", dayTracker)
    #st.write("day = " + day)
    availability_data.loc[dayTracker-1, 'day'] = day
    hourTracker = 1
    for hour in range(openTime, closeTime + 1):
        # Convert the hour to 12-hour format and determine AM or PM
        if hour < 12:
            am_pm = "AM"
            if hour == 0:
                hour = 12  # Midnight is 12 AM
        else:
            am_pm = "PM"
            if hour > 12:
                hour -= 12  # Convert to 1-based 12-hour clock
        time_str = f"{hour:02d}:00 {am_pm}"
        if day == "Monday":
            with colMonday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        elif day == "Tuesday":
            with colTuesday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        elif day == "Wednesday":
            with colWednesday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        elif day == "Thursday":
            with colThursday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        elif day == "Friday":
            with colFriday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        elif day == "Saturday":
            with colSaturday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        else:
            with colSunday:
                availStr = st.checkbox(time_str, key=day + ", " + time_str)
        #st.write("hourTracker = ", hourTracker)
        #st.write("availStr = ", availStr)
        availability_data.loc[dayTracker-1, hourTracker] = int(availStr == True)
        hourTracker = hourTracker + 1
    dayTracker = dayTracker + 1

# Create a submit button to save availability data to a CSV file
#availability_df = pd.DataFrame()
if st.button("Submit"):

    if playerName == "":
        st.error('You must enter your name!')
    else:
        playerNameShort = playerName.replace(' ', '_')
        # Save the DataFrame to a CSV file
        availability_data.to_csv("~/Documents/Python Programs/matchScheduler/userData/" +playerNameShort + "_availability.csv", index=False)
        st.success("Your availability has been saved to " + playerNameShort + "_availability.csv")

# Provide a download link for the generated CSV file
#st.write("Download your availability:")
#st.markdown("[Download user_availability.csv](data:file/csv;base64, " + availability_data.to_csv().encode('utf-8').decode(
#    'utf-8') + ")")

# Note: This code will save the availability data to a local file. In a real-world scenario, you might want to store this data more securely.
