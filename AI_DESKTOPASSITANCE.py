# importing all the usefull files
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import requests
import time
from win10toast import ToastNotifier
from urllib.request import urlopen
import json

# api key used for news
api_key = "44d202db90084dda90a97456658410e5"
# engine to set for speech_recognition
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# to get the audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# wishing msg acc to time


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("GOOD MORNING!")

    elif hour >= 12 and hour < 18:
        speak("GOOD AFTERNOON!")

    else:
        speak("GOOD EVENING!")

# Taking command from the user


def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_treshold = 1
        audio = r.listen(source)

    try:

        print("Rcognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said:{query}\n")

    except Exception as e:
        print(e)
        print("Say that again please")
        return "None"
    return query

# function to return news using newsapi


def news():
    main_url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=44d202db90084dda90a97456658410e5"
    news = requests.get(main_url).json()
    article = news["articles"]
    news_article = []
    for arti in article:
        news_article.append(arti['title'])

    return news_article

# function to find location


def location():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    return data


# Main function
if __name__ == "__main__":
    wishMe()
    speak("TELL ME YOUR COMMAND")
    while True:
        query = takeCommand().lower()
# To search anything from wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
# To find the location
        elif 'where am i' in query:
            data = location()
            speak(f"YOU are in {data['city'] ,data['region']}")
            print(f"YOU are in {data['city'] ,data['region']}")
# To open youtube in browser
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
# To open google in browser
        elif 'open google' in query:
            webbrowser.open("google.com")
# To open whatsapp in browser
        elif 'open whatsapp' in query:
            webbrowser.open("whatsapp.com")
# To open music from files
        elif 'play music' in query:
            music = 'C:\\Users\\anshu\\Music\\songs'
            songs = os.listdir(music)
            print(songs)
            ran = random.randint(0, 1)
            print(ran)
            os.startfile(os.path.join(music, songs[ran]))
# To find the time
        elif 'the time' in query:
            strdate_time = datetime.datetime.now().strftime("%Y-%M-%D %H:%M:%S")
            speak(f"hello,The date and  time is {strdate_time}")
# To output first 3 news
        elif 'tell me news' in query:
            new = news()
            for i in range(3):
                print(new[i])
                speak(new[i])
# to set timers
        elif 'set timer' in query:
            toaster = ToastNotifier()
            speak("what is title of the timer")
            title = takeCommand()
            speak("what is your message ")
            msg = takeCommand()
            time_inp = {'one': 1, 'two': 2, 'five': 5, 'ten': 10}
            speak("please type youe time in minutes below")
            minutes = float(input("timer for how many minutes"))
            print(minutes)

            sec = 60*minutes

            speak(f"timer set for {minutes} minutes!")
            time.sleep(sec)
            toaster.show_toast(title, msg, duration=10, threaded=True)

            while toaster.notification_active:
                time.sleep(0.1)
# To exit the program
        elif 'quit' in query:
            speak("Thankyou!byee")
            exit()
