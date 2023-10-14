import streamlit as st
import pandas as pd

# Create a Streamlit web app
st.title("Availability Scheduler")

# Create a form to collect user availability data
st.write("Check which times you are available for each day of the week:")

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']# Define the start and end times
colMonday, colTuesday, colWednesday, colThursday, colFriday, colSaturday, colSunday = st.columns(7)
dayCols = []
for day in days_of_week:
	dayCols.append("col" + day)
st.write(dayCols[0])

openTime = 8  # 8 AM
closeTime = 21  # 9 PM

availability_data = {}
for day in days_of_week:
    for hour in range(openTime, closeTime+1):
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
        with dayCols[0]:
            availStr = st.checkbox(day + ", " + time_str)
    availability_data[day, hour] = availStr

# Create a submit button to save availability data to a CSV file
availability_df = pd.DataFrame()
if st.button("Submit"):
    # Create a DataFrame from the availability data
    availability_df = pd.DataFrame(availability_data, index=[0])

    # Save the DataFrame to a CSV file
    availability_df.to_csv("user_availability.csv", index=False)
    st.success("Your availability has been saved to user_availability.csv")

# Provide a download link for the generated CSV file
st.write("Download your availability:")
st.markdown("[Download user_availability.csv](data:file/csv;base64, " + availability_df.to_csv().encode('utf-8').decode('utf-8') + ")")

# Note: This code will save the availability data to a local file. In a real-world scenario, you might want to store this data more securely.