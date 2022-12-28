import openai
openai.api_key = "put api key here"

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser

import os
import random

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

import requests, json

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")



#register chrome as default web browser
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# for voice in voices:
#     print(f"Voice: {voice.name}")
engine.setProperty('voice',voices[3].id)




#speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def intro():
    hour = int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        speak("Good Morning!")
    elif hour >=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant Drishti, How may I help you ?")

def takeCommand():
    #audio to string
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") 
        r.pause_threshold=1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None_354465"    #coded string    
    
    return query

#to get current location
def getLocation():
    options = Options()
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    timeout = 20
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)
      
    longitude = driver.find_elements("xpath", '//*[@id="longitude"]') 
    longitude = [x.text for x in longitude]    
    longitude = str(longitude[0])    
    latitude = driver.find_elements("xpath", '//*[@id="latitude"]') 
    latitude = [x.text for x in latitude]    
    latitude = str(latitude[0])    
    driver.quit() 
    print(latitude,longitude)
    location = geolocator.reverse(latitude+","+longitude)
    print(location)
    return(latitude,longitude,location)

def getweather():

    api_key = 'openweather_api_key_here'
    lat = getLocation()[0]
    lon = getLocation()[1]

    complete_url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":

        y = x["main"]
        current_temperature = y["temp"]-273.15
        current_pressure = y["pressure"]/1000.0
        current_humidity = y["humidity"]

        z = x["weather"]
        weather_description = z[0]["description"]

        # print following values
        print(" Temperature (in celsius unit) = " +
                        str(current_temperature) +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidity) +
            "\n description = " +
                        str(weather_description))
        
        speak(f"According to OpenWeatherMap.org {weather_description} is expected at your location " +
              f"\n with current temperature of {current_temperature} degrees celsius " +
              f"\n Atmospheric pressure is {current_pressure} bar and humidity is {current_humidity} percent")

    else:
        print("Sorry, Weather Report not found")
        speak("Sorry, Weather Report not found")

#chatgpt integration
def gpt_response(query):
    model_engine = "text-davinci-003"

    response = openai.Completion.create(
    engine=model_engine,
    prompt=query,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,)
    response = response.choices[0].text
    print(response)
    return response





     
    

if __name__ =="__main__":
    intro()
    flag = 0    #to check if last response of bot was successful
    while True:
        query = takeCommand().lower()
        

        #logic for executing tasks on query
        if 'drishti stop' in query:
            break

        elif 'gpt' in query:
            speak(gpt_response(query))

            flag =0

        elif 'wikipedia'  in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences = 2)
            speak("According to Wikipedia,")
            print(results)
            speak(results)

            flag=0

        elif 'play music' in query:
            music_dir = 'pathto\d_bot\music'
            songs = os.listdir(music_dir)
            print(songs)
            play =  random.choice(songs)   
            os.startfile(os.path.join(music_dir, play))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

            flag =0
        
        elif 'my location' in query:
            speak(f"Your current location is {getLocation()[2]}")

            flag =0

        elif 'weather' in query:
            getweather()

            flag=0
        

        elif query != "None_354465":
            if flag == 0:
                speak("Sorry I can't help with that. Please try again ...")
                flag = 1

            
        
