import os
import subprocess as sp
import random
import time
from datetime import datetime
import webbrowser
import pyttsx3
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Paths for applications
paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\lolik\\AppData\\Local\\Discord\\app-1.0.9173\\Discord.exe",  # Update path
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

# Function to speak a message
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

# Function to fetch weather info (uses OpenWeatherMap API)
def get_weather(city):
    api_key = "f59f5f32d351ec9ad072e249b16d8b27"  # Get an API key from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]["description"]
        temperature = main["temp"]
        return f"{weather} with a temperature of {temperature}°C"
    else:
        return "City not found"

# Function to set an alarm
def set_alarm(alarm_time):
    alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
    current_time = datetime.now()
    alarm = datetime(current_time.year, current_time.month, current_time.day, alarm_hour, alarm_minute)
    while datetime.now() < alarm:
        time.sleep(10)  # Check every 10 seconds
    speak(f"Alarm! It's {alarm_time}. Time to wake up!")

# Function to play music (using web browser to play YouTube)
def play_music(song_name):
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    webbrowser.open(search_url)

# Function to shut down the system
def shutdown_system():
    os.system('shutdown /s /f /t 1')

# Function to open the default web browser
def open_browser():
    webbrowser.open("https://www.google.com")

# Function to take a note (saves to a text file)
def take_note(note_content):
    with open("notes.txt", "a") as note_file:
        note_file.write(note_content + "\n")

# Function to set a reminder (saves to a text file)
def set_reminder(task, reminder_time):
    with open("reminders.txt", "a") as reminder_file:
        reminder_file.write(f"Reminder: {task} at {reminder_time}\n")
    speak(f"I'll remind you about '{task}' at {reminder_time}")

# Function to translate text (uses Google Translate API)
def translate_text(sentence, language):
    from googletrans import Translator
    translator = Translator()
    translated = translator.translate(sentence, dest=language)
    return translated.text

# Function to get word definition (uses Merriam-Webster API)
def get_word_definition(word):
    api_key = "8bfbe1c7-5053-49d6-98ef-203617eb6def"  # Get an API key from Merriam-Webster
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        definition = data[0]["shortdef"][0]
        return definition
    else:
        return "Word not found"

# Functions for opening applications
def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    os.startfile(paths['notepad'])

def open_discord():
    os.startfile(paths['discord'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])

# Fun interactions (Joke and Advice)
def get_random_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    return random.choice(jokes)

def get_random_advice():
    advices = [
        "Don't take life too seriously, nobody gets out alive anyway.",
        "Believe in yourself and all that you are.",
        "If you want something you've never had, you must be willing to do something you've never done."
    ]
    return random.choice(advices)
