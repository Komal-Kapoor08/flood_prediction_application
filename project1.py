import streamlit as st
import pandas as pd
import requests
import smtplib
from email.message import EmailMessage
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import googletrans
from googletrans import Translator



df = pd.read_csv("fp.csv")


X = df[['Rainfall (mm)', 'Temperature (°C)', 'Humidity (%)']]
y = df['Flood Occurred']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)



st.title("🌊 FloodAware System")
st.write("Check flood predictions for your city. Be aware, Be Prepared, stay safe.")

city = st.text_input("🏙️ Enter City:")
user_email = st.text_input(" 📧 Enter Your Email to receive alerts:")



def fetch_weather(city):
    api_key = "cb20db119f87e2865dc6567da7f697bc"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.json()
        humidity = weather["main"]["humidity"]
        temperature = weather["main"]["temp"]
        rainfall = weather.get("rain", {}).get("1h", 0)
        return humidity, rainfall, temperature
    else:
        st.error(" Failed to fetch weather data.")
        return None



def send_email(recipient):
    english_msg = "Flood risk detected in your area. Stay safe and follow emergency protocols."
    
    translator = Translator()
    translated = translator.translate(english_msg, dest='hi')
    hindi_msg = translated.text

    full_msg = f" Flood Alert!\n\nENGLISH:\n{english_msg}\n\nहिंदी:\n{hindi_msg}"

    msg = EmailMessage()
    msg['Subject'] = " Flood Alert!"
    msg['From'] = "komalkapoor0806@gmail.com"
    msg['To'] = recipient
    msg.set_content(full_msg)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("komalkapoor0806@gmail.com", "pjku kwba cemj lktj")
        smtp.send_message(msg)



if st.button(" 🔍Check Flood Risk"):
    if city:
        result = fetch_weather(city)
        if result:
            humidity, rainfall, temperature = result

            st.write(f"💧Humidity: {humidity}%")
            st.write(f"🌧️Rainfall: {rainfall} mm")
            st.write(f"🌡️Temperature: {temperature}°C")


            input_data = [[rainfall, temperature, humidity]]
            prediction = model.predict(input_data)

            if prediction[0] == 1:
                st.error("🚨 Flood Alert: Risk of Flooding Detected!")
                if user_email:
                    send_email(user_email)
                    st.success(f"✉️ Alert sent to {user_email} in English & Hindi.")
            else:
                st.success(" No Flood Expected. You are Safe.")
    else:
        st.warning(" Please enter a city name.")

hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)
