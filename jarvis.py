import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import time
import requests
import random
import math
import pyjokes
import pywhatkit
import wikipedia

# Initialize the speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Adjust the recognizer for ambient noise
with sr.Microphone() as source:
    print("Calibrating ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=5)
    print("Ambient noise calibrated.")

# Function to speak out the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=3):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=timeout)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            print("You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            print("Timeout occurred, no speech detected within the specified duration.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            print(f"Failed to request speech recognition service: {e}")
            return ""



# Function to play a song by name
def play_song(song_name):
    # You can replace this with your own music directory
    music_dir = "C:/Music"
    songs = os.listdir(music_dir)
    for song in songs:
        if song_name.lower() in song.lower():
            os.startfile(os.path.join(music_dir, song))
            break
    else:
        speak("Sorry, I couldn't find the song.")

# Function to show map with given location
def show_map(location):
    url = f"https://www.google.com/maps/search/{location}"
    webbrowser.open(url)

# Function to get weather information for a given city
def get_weather(city_name):
    api_key = "888e0a98dd160b5751105a60a4f9af43"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        speak(f"The weather in {city_name} is {weather_desc}. The temperature is {temp} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

# Function to tell a random joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def search_wikipedia(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        speak(f"There are multiple options for {topic}. Here are a few: {', '.join(options[:3])}")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find any information on {topic}.")

# Function to perform a general Google search
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

# Function to set an alarm
def set_alarm(hour, minute):
    current_time = datetime.datetime.now()
    alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
    time_diff = alarm_time - current_time
    alarm_seconds = time_diff.total_seconds()

    if alarm_seconds < 0:
        speak("The provided time has already passed.")
        return

    time.sleep(alarm_seconds)
    speak("Alarm!")
    # You can add additional actions here, such as playing a sound or displaying a notification

# Function to set a timer
def set_timer(minutes):
    seconds = minutes * 60
    time.sleep(seconds)
    speak("Timer finished!")
    # You can add additional actions here, such as playing a sound or displaying a notification

# Main function to handle commands
def main():
    speak("Hello")
    print("How can I help you today?")
    while True:
        query = listen()

        if "hello" in query:
            speak("Hello! How can I assist you today?")

        elif "what is your name" in query:
            speak("I am your virtual assistant.")

        elif "how are you" in query:
            speak("I'm fine, thank you for asking!")

        elif "play song" in query:
            speak("Sure, what is the name of the song?")
            song_name = listen()
            play_song(song_name)

        elif "show map" in query:
            speak("Sure, which location's map do you want to see?")
            location = listen()
            show_map(location)

        elif "weather" in query:
            speak("Sure, for which city do you want to know the weather?")
            city_name = listen()
            get_weather(city_name)

        elif "joke" in query:
            tell_joke()

        elif "set alarm" in query:
            speak("At what time do you want to set the alarm?")
            speak("Please say the hour.")
            hour = int(listen())
            speak("Please say the minute.")
            minute = int(listen())
            set_alarm(hour, minute)

        elif "set timer" in query:
            speak("For how many minutes do you want to set the timer?")
            minutes = int(listen())
            set_timer(minutes)

        elif 'play' in query:
            song = query.replace('play', '').strip()  # Extract song name from query
            speak('Playing ' + song)
            pywhatkit.playonyt(song)

        elif "exit" in query or "bye" in query:
            speak("Goodbye!")
            break
        
        elif "search wikipedia" in query:
            topic = query.replace("search wikipedia", "").strip()
            search_wikipedia(topic)

        elif "search" in query:
            search_query = query.replace("search", "").strip()
            google_search(search_query)


        else:
            speak("Sorry, I couldn't understand that.")

if __name__ == "__main__":
    main()
