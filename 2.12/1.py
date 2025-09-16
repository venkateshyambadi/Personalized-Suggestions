import streamlit as st
from streamlit_option_menu import option_menu
from database import fetch_user
import pandas as pd
import pandas as pd 
from nltk.tokenize import word_tokenize
from nltk.downloader import download, download_shell
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
import streamlit as st
import sqlite3
from db import add_user_data, fetch_user_data,delete_medication,update_medication,all_data
from streamlit_option_menu import option_menu 
import requests
download('stopwords')
download('punkt')
import streamlit as st
import pandas as pd
import datetime
import calendar
from playsound import playsound
ps = PorterStemmer()
STOPWORDS = stopwords.words('english')
new_word = ["having","feel",'symptoms','symptoms','experiencing','experienced','feeling']
STOPWORDS.extend(new_word)
import speech_recognition as sr
from googletrans import Translator
def speech_to_text():
    recognizer = sr.Recognizer()
    translator = Translator()
    with sr.Microphone() as source:
        st.write("Say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            translation = translator.translate(text, src='auto', dest='en')
            return translation.text
        except sr.UnknownValueError:
            return "Sorry, could not understand audio."
        except sr.RequestError as e:
            return "Could not request results; {0}".format(e)

df = pd.read_csv('NAFDAC-DRUGS.csv',usecols = ['NAME_OF_PRODUCT','USE_OF_DRUG','IMAGE'])
df_dict = df.set_index('NAME_OF_PRODUCT').T.to_dict('list')
list_drug_symptoms = [i[0] for i in list(df_dict.values())]
list_drug_images = [i[1] for i in list(df_dict.values())]

conn = sqlite3.connect('data.db')
YOUTUBE_API_KEY = "AIzaSyDYEeSTrT7pPpVzpmaJ491gxogVxfWwpvM"
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def fetch_youtube_videos(query, max_results=12):
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': YOUTUBE_API_KEY,
        'maxResults': max_results
    }
    response = requests.get(url, params=params)
    videos = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            videos.append({'video_id': video_id, 'title': video_title})
    return videos

def user_home_page():
    user = fetch_user(st.session_state["current_user"])
    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 👋 {user[1]}</h1>", unsafe_allow_html=True)
        if user[4]=='Male👦🏻':
            st.markdown(
                """
                <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                    <i
                    mg src="https://cdn-icons-png.flaticon.com/512/2621/2621983.png" width="200">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2621/2621983.png" width="200">
                </div>
                """,
                unsafe_allow_html=True
            )
        select = option_menu(
            "",
            ["Patient Profile",'Medicine Recommendations','Traditional Remedies','Remainder Alert','Remainder calendar',"Logout"],
            icons=['person-square','eye-fill','file-earmark-fill','question-circle-fill' ,'lock-fill'],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0", "background-color": "#d6d6d6"}, 
                "icon": {"color": "black", "font-size": "20px"},    
                "nav-link": {
                    "font-size": "16px",
                    "margin": "0px",
                    "color": "black",                                          
                },   
                "nav-link-selected": {
                    "background-color": "#10bec4",                            
                },
            },
        )

    if select == 'Patient Profile':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images5.alphacoders.com/135/1351189.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        # Extracting user data from session state after successful login
        if user:
            # Assuming 'user' is a tuple (id, name, email, password, regd_no, year_of_study, branch, student_type, student_image)
            name, age, gender = user[1], user[3], user[4]
            if gender == 'Male👦🏻':
                image_link = "https://img.freepik.com/photos-premium/elevez-votre-marque-avatar-amical-qui-reflete-professionnalisme-ideal-pour-directeurs-ventes_1283595-18531.jpg?semt=ais_hybrid"
            else:
                image_link = "https://cdn-icons-png.flaticon.com/512/219/219969.png"

            # CSS Styling for vertical container
            profile_css = """
            <style>
                .profile-container {
                    background-image: url('https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjg1OC1rdWwtMDIuanBn.jpg');
                    background-size: cover;
                    background-position: center;
                    padding: 50px;
                    border-radius: 50px;
                    box-shadow: 10px 8px 12px rgba(0, 0, 0, 0.15);
                    max-width: 400px;
                    border: 2px solid black;
                    margin-left: 100%;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .profile-header {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 1px;
                    color: #333;
                }
                .profile-item {
                    font-size: 18px;
                    margin-bottom: 10px;
                    color: #555;
                }
                .profile-image img {
                    border-radius: 50%;
                    max-width: 250px;
                    max-height: 250px;
                    margin-bottom: 0px;
                }
            </style>
            """

            # HTML Structure for vertical alignment
            profile_html = f"""
            <div class="profile-container">
                <div class="profile-image">
                    <img src="{image_link}" alt="User Image">
                </div>
                <div class="profile-details">
                    <div class="profile-header">User Report</div>
                    <div class="profile-item"><strong>Name:</strong> {name}</div>
                    <div class="profile-item"><strong>Age:</strong> {age}</div>
                    <div class="profile-item"><strong>Gender:</strong> {gender}</div>
                </div>
            </div>
            """

            # Display styled content
            st.markdown(profile_css + profile_html, unsafe_allow_html=True)
    elif select == 'Medicine Recommendations':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://i.pinimg.com/736x/88/cb/21/88cb21d0fa57c354f52615d46a821b41.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.title('Medicine Recommendation System')
        text = st.text_area(label ='Enter the symptoms you are experiencing.',placeholder = 'E.g headache, stomach pain, diarrhea, body pain,fever,cold,hypertension e.t.c',height=20)
        field_names = ['having','feel','symptoms','symptoms','experience','experiencing']

        empty = []
        token_length = []
        def similarity(my_word):
            my_word = my_word.lower()
            my_word = re.sub(r'[^\w\s]', ' ',my_word)
            my_word = word_tokenize(my_word)
            my_word_tokens = [ps.stem(word1) for word1 in my_word if word1 not in STOPWORDS]

            for i in list_drug_symptoms:
                drug_symptom = i.lower()
                drug_symptom = re.sub(r'[^\w\s]', ' ',drug_symptom)
                drug_symptom = word_tokenize(drug_symptom)
                drugs_symptom_tokens = [ps.stem(word) for word in drug_symptom if word not in STOPWORDS]
                a_token_len = len(drugs_symptom_tokens)
                my_set = set.intersection(set(my_word_tokens),set(drugs_symptom_tokens))
                set_len = len(my_set)
                empty.append(set_len)
                token_length.append(a_token_len)
            return (empty,token_length) # returns a tuple

        if st.button('Recommend'):
            my_ratios = similarity(text)
            freq = my_ratios[0]
            token_len = my_ratios[1]
            my_drug_names = list(df_dict.keys())
            my_drug_images = list_drug_images
            my_result = [my_drug_names,freq,token_len,my_drug_images]
            my_result_df = pd.DataFrame(my_result).T
            my_result_df.columns = ['Drug_Names','Freqtokens','drug_t_len','drug_images']
            sorted_result_df= my_result_df.sort_values(by=['Freqtokens','drug_t_len'],ascending=[False, True])
            top5 = sorted_result_df.head(6)

            while text:
                if sorted_result_df['Freqtokens'].sum() == 0:
                    st.write('There are no drugs to recommend you at this time.')
                    result = 'There are no drugs to recommend you at this time.'
                    break
            
                else: 
                    st.write('**Here are the recommended drugs for the symptoms you are experiencing**')
                    
                    result = ','.join(top5['Drug_Names'].tolist())
                
                    drug1,drug2,drug3 = st.columns(3)

                    #IMAGES
                    with drug1:
                        st.write(top5.iloc[0,0])
                        st.image(top5.iloc[0,3])
                    
                    with drug2:
                        st.write(top5.iloc[1,0])
                        st.image(top5.iloc[1,3])

                    with drug3:
                        st.write(top5.iloc[2,0])
                        st.image(top5.iloc[2,3])
                    st.markdown('---')
                    drug1,drug2,drug3 = st.columns(3)
                    with drug1:
                        st.write(top5.iloc[3,0])
                        st.image(top5.iloc[3,3])

                    with drug2:
                        st.write(top5.iloc[4,0])
                        st.image(top5.iloc[4,3])
                    with drug3:
                        st.write(top5.iloc[5,0])
                        st.image(top5.iloc[5,3])
                        break
            else:
                st.subheader('Please Enter a valid response!')
                result = 'Please Enter a valid response!'
    elif select == 'Traditional Remedies':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://png.pngtree.com/thumb_back/fh260/background/20231105/pngtree-top-view-of-herbal-medicine-pills-on-white-textured-background-embracing-image_13739055.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.title('Traditional Home Remedies')
        text = st.text_area(label ='Enter the symptoms you are experiencing.',placeholder = 'E.g headache, stomach pain, diarrhea, body pain,fever,cold,hypertension e.t.c',height=20)
        st.button('Search',type='primary')
        if text:
            videos = fetch_youtube_videos(text+' traditional home remedies', max_results=10)
            # Display videos in rows of 3
            for i in range(0, len(videos), 2):
                cols = st.columns(2)  # Create 3 columns
                for j, video in enumerate(videos[i:i+2]):  # Iterate over videos for the current row
                    with cols[j]:
                        st.video(f"https://www.youtube.com/watch?v={video['video_id']}")
    
    elif select == 'Remainder Alert':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://health.wyo.gov/wp-content/uploads/2020/08/bullhorn-alert-with-yellow-background.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        option=['View Medication','Add Medidaton','Delete Medication','Update Medication']
        select = st.selectbox('Select Option',option)
        if select == 'View Medication':
            data=fetch_user_data(user[2])
            if data:
                st.header('Your Medication Reminders 🚨')
                # Display the medication reminders 1st give medidation name, 2nd give start date, 3rd give time, 4th give days
                df = pd.DataFrame(data, columns=["Name", "Start Date", "Time", "Medication", "Days"])

                for index, row in df.iterrows():
                    # Adding a red header

                    # Writing details in black text
                    st.markdown(f"<p style='color:black;'>Medication: {row['Medication']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:black;'>Start Date: {row['Start Date']}</p>", unsafe_allow_html=True)
                    
                    # Calculate end date
                    end_date = pd.to_datetime(row["Start Date"]) + datetime.timedelta(days=row["Days"] - 1)
                    st.markdown(f"<p style='color:black;'>End Date: {end_date.date()}</p>", unsafe_allow_html=True)
                    
                    # Convert time to AM/PM format
                    time_obj = datetime.datetime.strptime(row["Time"], "%H:%M:%S")
                    time_am_pm = time_obj.strftime("%I:%M %p")
                    st.markdown(f"<p style='color:black;'>Time: {time_am_pm}</p>", unsafe_allow_html=True)
                    
                    # Add a separator
                    st.markdown('---')

            else:
                st.write('No Medication Reminders Found')
        elif select == 'Add Medidaton':
            id=user[0]
            mail=user[2]
            # Input Section
            st.header("Add Medication Reminder ⏰")
            start_date = st.date_input("Select Start Date", datetime.date.today(), min_value=datetime.date.today())
            time = st.time_input("Select Time", datetime.time(9, 0))
            medication = st.text_input("Medication Name")
            days = st.number_input("Number of Days to Take Medication", min_value=1, value=1, step=1)
            
            if st.button("Save Reminder"):
                add_user_data(mail,start_date,time,medication,days)
                st.success(f'Successfully added {medication} reminder for {days} days starting from {start_date} at {time}')
        elif select == 'Delete Medication':
            st.subheader("Delete Medication Reminder 🗑️")
            data=fetch_user_data(user[2])
            if data:
                # Display the medication reminders
                df = pd.DataFrame(data, columns=["Name", "Start Date", "Time", "Medication", "Days"])
                medication_names = df["Medication"].unique()
                mail=user[2]
                medication = st.selectbox("Select Medication to Delete", medication_names)
                if st.button("Delete Reminder"):
                    delete_medication(mail,medication)
                    st.success(f"Successfully deleted {medication} reminder")
            else:
                st.write('No Medication Reminders Found')
        elif select == 'Update Medication':
            st.subheader("Update Medication Reminder 🔄")
            data=fetch_user_data(user[2])
            if data:
                # Display the medication reminders
                df = pd.DataFrame(data, columns=["Name", "Start Date", "Time", "Medication", "Days"])
                medication_names = df["Medication"].unique()
                mail=user[2]
                medication = st.selectbox("Select Medication to Update", medication_names)
                new_days = st.number_input("Number of New Days to Take Medication", min_value=1, value=1, step=1)
                if st.button("Update Reminder"):
                    update_medication(mail,medication,new_days)
                    st.success(f"Successfully updated {medication} reminder for {new_days} days.")
            else:
                st.write('No Medication Reminders Found')



    elif select == 'Remainder calendar':
        all_data()
        data=fetch_user_data(user[2])
        date=data[0][1]
        time=data[0][2]
        medication=data[0][3]
        days=data[0][4] 
        current_date = datetime.date.today()
        current_datetime = datetime.datetime.now()

        # Streamlit app setup
        st.title("Medication Alert System")

        alert_triggered = False  # To track if any alert is displayed

        for record in data:
            email, date_str, time_str, medication, days = record
            
            # Parse the date and time strings
            record_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            record_time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
            
            # Convert record_time to a datetime object for comparison
            record_datetime = datetime.datetime.combine(record_date, record_time)
            
            # Check if the date matches and the time is within 2 hours before
            time_difference = (record_datetime - current_datetime).total_seconds()
            if record_date == current_date and 0 <= time_difference <= 2 * 3600:  # Time is within 2 hours before
                alert_triggered = True
                st.warning(f"⚠️ It's time for your medication: **{medication}** at **{time_str}**!")

        if not alert_triggered:
            st.info("No medication alerts at the moment.")
    


        #fetching user data
        def generate_color_map(data):
            medications = set(row[3] for row in data)  # Get unique medication names
            colors = ['#FF6347', '#8A2BE2', '#32CD32', '#FFD700', '#FF4500', '#2E8B57', '#C71585']
            color_map = {medication: colors[i % len(colors)] for i, medication in enumerate(medications)}
            return color_map

        # Function to mark the calendar days and handle overlapping dates
        def get_medication_days(data, today, n_days):
            end_date = today + datetime.timedelta(days=n_days)
            medication_days = {}  # Dictionary to store medication days with their colors

            # Generate the medication days with respective colors
            for row in data:
                medication_date = pd.to_datetime(row[1]).date()
                medication_color = color_map.get(row[3], '#000000')  # Default to black if no color found
                days_of_medication = row[4]

                # Mark the days for the given range of medication
                for day_offset in range(days_of_medication):
                    medication_day = medication_date + datetime.timedelta(days=day_offset)
                    if today <= medication_day <= end_date:
                        if medication_day.month not in medication_days:
                            medication_days[medication_day.month] = {}
                        if medication_day.day not in medication_days[medication_day.month]:
                            medication_days[medication_day.month][medication_day.day] = []
                        medication_days[medication_day.month][medication_day.day].append((row[3], medication_color))
            
            return medication_days

        # Fetch current date
        today = datetime.date.today()

        # Define the number of days to consider (e.g., next 100 days)
        n_days = 100

        # Generate color map for the medications
        color_map = generate_color_map(data)

        # Fetch medication days with respective colors
        medication_days = get_medication_days(data, today, n_days)

        # Display the color map for medication names and colors at the top
        st.markdown("<h2>Medication Calendar📆</h2>", unsafe_allow_html=True)
        num_items = len(color_map)
        cols = st.columns(num_items)

        # Iterate over the color_map and place each item in its column
        for idx, (medication, color) in enumerate(color_map.items()):
            with cols[idx]:
                st.markdown(
                    f'<span style="color:{color}; font-weight: bold; margin-right: 10px;">{medication}</span>',
                    unsafe_allow_html=True
                )

        # Define CSS for styling the calendar
        st.markdown(
            """
            <style>
                .calendar-container {
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 20px;
                }
                .calendar-month {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    background-color: #f9f9f9;
                }
                .calendar-title {
                    text-align: center;
                    font-weight: bold;
                    font-size: 18px;
                    margin-bottom: 10px;
                    background-color: #f2c13a;
                }
                .calendar-table {
                    width: 100%;
                    text-align: center;
                    border-collapse: collapse;
                    margin: 0 auto;
                }
                .calendar-table th, .calendar-table td {
                    padding: 5px;
                    border: 1px solid #ddd;
                }
                .calendar-table th {
                    background-color: #f4f4f4;
                    font-weight: bold;
                }
                .medication-day {
                    font-weight: bold;
                }
                .overlapping-day {
                    font-weight: bold;
                    color: #000000;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Display calendars for each month within the range of medication days
        for month in medication_days.keys():
            with st.container():
                st.markdown('<div class="calendar-month">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="calendar-title">{calendar.month_name[month]} {today.year}</div>',
                    unsafe_allow_html=True,
                )

                cal = calendar.monthcalendar(today.year, month)
                
                calendar_html = '<table class="calendar-table">'
                calendar_html += (
                    "<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>"
                )
                for week in cal:
                    calendar_html += "<tr>"
                    for day in week:
                        if day == 0:
                            calendar_html += "<td></td>"
                        else:
                            # Check if the day is in the medication days for this month
                            if day in medication_days[month]:
                                # If multiple medications overlap on the same day
                                if len(medication_days[month][day]) > 1:
                                    calendar_html += f'<td class="overlapping-day">{day}<br><ul>'
                                    calendar_html += '</ul></td>'
                                else:
                                    medication_color = medication_days[month][day][0][1]
                                    calendar_html += f'<td class="medication-day" style="color: {medication_color};">{day}</td>'
                            else:
                                calendar_html += f"<td>{day}</td>"
                    calendar_html += "</tr>"
                calendar_html += "</table>"

                st.markdown(calendar_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)


    elif select == 'Logout':
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        navigate_to_page("home")
