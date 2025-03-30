import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from functions.online_ops import (
    find_my_ip, get_random_advice, get_random_joke, 
    play_on_youtube, search_on_google, search_on_wikipedia, 
    send_email, send_whatsapp_message, get_weather)
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from decouple import config
import threading
import math
import re
from fuzzywuzzy import fuzz

# Predefined list of cities for weather (add as many as you like)
PREDEFINED_CITIES = ['Pardubice', 'Prague', 'London', 'New York', 'Los Angeles', 'Tokyo', 'Berlin']
def evaluate_expression(expression):
    try:
        # Evaluate the mathematical expression (safe evaluation)
        result = eval(expression)
        return result
    except Exception as e:
        speak("Sorry, I couldn't understand the math expression.")
        print(f"Error evaluating expression: {e}")
        return None
# Function to get the closest city match
def get_closest_city(query):
    best_match = None
    highest_score = 0

    # Compare user input with predefined cities using fuzzy matching
    for city in PREDEFINED_CITIES:
        score = fuzz.ratio(query.lower(), city.lower())
        if score > highest_score:
            highest_score = score
            best_match = city

    # If the score is above a certain threshold, return the match
    if highest_score > 75:  # This can be adjusted as needed
        return best_match
    else:
        return None

def initialize_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    return engine

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet_user():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}")
    else:
        speak("Good Night!")
    speak(f"I am {BOTNAME}. How may I assist you?")

# Function to take voice input from the user
def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        r.pause_threshold = 1  # Set the pause threshold to 1 second

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in', show_all=False)
            print(f"User said: {query}")

            # Check if the query is related to weather
            if "weather" in query:
                speak("Which city do you want the weather information for?")
                city_query = take_user_input()
                city = get_closest_city(city_query)

                if city:
                    speak(f"Did you mean {city}?")
                    confirm_query = take_user_input()
                    if 'yes' in confirm_query:
                        weather_info = get_weather(city)
                        speak(weather_info)
                        print(weather_info)
                    else:
                        speak("Please provide the city name again.")
                else:
                    speak("I couldn't recognize the city. Could you please repeat?")
            else:
                return query.lower()
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything. Could you please repeat?")
            return 'None'
        except sr.RequestError:
            speak("Sorry, I couldn't reach the server. Please try again later.")
            return 'None'
        except Exception as e:
            print(f"Error: {e}")
            speak('Sorry, I could not understand. Could you please say that again?')
            return 'None'

    return query.lower()

# Initialize variables
USERNAME = config('USER')
BOTNAME = config('BOTNAME')
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize PyAutoGUI screen dimensions
screen_width, screen_height = pyautogui.size()

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Initialize variables for smoothing
previous_x, previous_y = None, None  # Initialized to None
smooth_factor = 0.6  # Smoothing factor for cursor movement

# Scale factors for virtual screen size
scale_factor_x = 1.8  # Horizontal scale
scale_factor_y = 0.75  # Vertical scale (adjust this for easier hand movement)

# Function to check if a pinch gesture is detected
def is_pinch(hand_landmarks, frame_width, frame_height):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    
    index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
    thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    
    # Calculate the distance between thumb and index finger tips
    distance = np.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)
    
    # A threshold value for the pinch (could be adjusted)
    return distance < 27

# Function to check if middle and thumb fingers are together
def is_middle_thumb_together(hand_landmarks, frame_width, frame_height):
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    
    middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)
    thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    
    # Calculate the distance between middle and thumb tips
    distance = np.sqrt((middle_x - thumb_x) ** 2 + (middle_y - thumb_y) ** 2)
    
    return distance < 24

# Function to handle voice recognition in a separate thread
def voice_recognition_thread():
    while True:
        query = take_user_input()

        if 'hello' in query:
            speak('Hello! How can I help you?')

        # Apps and utilities
        elif 'open notepad' in query:
            open_notepad()
        elif 'open discord' in query:
            open_discord()
        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()
        elif 'open camera' in query:
            open_camera()
        elif 'open calculator' in query:
            open_calculator()
        elif 'plus' in query or 'minus' in query or 'times' in query or 'divided by' in query:
            # Convert verbal math operations to symbols
            query = query.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')

            # Now evaluate the expression
            result = evaluate_expression(query)
    
            if result is not None:
                speak(f"The result is {result}")
                print(f"Result: {result}")
            else:
                speak("I couldn't calculate that.")

        # IP Address
        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}')
            print(f'Your IP Address is {ip_address}')

        # Set alarm
        elif 'set alarm' in query:
            speak("At what time do you want to set the alarm? Please say the time in HH:MM format.")
            alarm_time = take_user_input()
            set_alarm(alarm_time)
            speak(f"Alarm has been set for {alarm_time}")
            
        # Weather
        elif 'weather' in query:
            speak("Which city's weather do you want to know about?")
            city = take_user_input()
            weather_info = get_weather(city)
            speak(f"The weather in {city} is {weather_info}")
            print(weather_info)

        # Time
        elif 'time' in query:
            current_time = get_current_time()
            speak(f"The current time is {current_time}")
            print(f"The current time is {current_time}")
        
        # Wikipedia search
        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia?')
            search_query = take_user_input()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            print(results)  # Print for convenience

        # YouTube search and playback
        elif 'youtube' in query:
            speak('What do you want to play on Youtube?')
            video = take_user_input()
            play_on_youtube(video)

        # Google search
        elif 'search on google' in query:
            speak('What do you want to search on Google?')
            g_query = take_user_input()
            search_on_google(g_query)

        # Sending WhatsApp message
        elif "send whatsapp message" in query:
            speak('On what number should I send the message? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message?")
            message = take_user_input()
            send_whatsapp_message(number, message)
            speak("I've sent the message.")

        # Sending email
        elif "send an email" in query:
            speak("On what email address do I send it? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject?")
            subject = take_user_input()
            speak("What is the message?")
            message = take_user_input()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email.")
            else:
                speak("Something went wrong while I was sending the mail.")

        # Fun interactions
        elif 'joke' in query:
            speak("Hope you like this one.")
            joke = get_random_joke()
            speak(joke)
            print(joke)

        elif "advice" in query:
            speak("Here's an advice for you.")
            advice = get_random_advice()
            speak(advice)
            print(advice)

        # Play music
        elif 'play music' in query:
            speak("What music would you like to listen to?")
            song_name = take_user_input()
            play_music(song_name)
            speak(f"Playing {song_name}")

        # Shutdown system
        elif 'shutdown' in query:
            speak("Are you sure you want to shut down the system?")
            confirmation = take_user_input()
            if 'yes' in confirmation:
                shutdown_system()
                speak("Shutting down now.")

        # Open browser
        elif 'open browser' in query:
            open_browser()
            speak("Opening your web browser.")

        # Take note
        elif 'take note' in query:
            speak("What do you want to note down?")
            note_content = take_user_input()
            take_note(note_content)
            speak("Your note has been saved.")

        # Set reminder
        elif 'remind me' in query:
            speak("What should I remind you about?")
            task = take_user_input()
            speak("When should I remind you?")
            reminder_time = take_user_input()
            set_reminder(task, reminder_time)
            speak(f"I'll remind you about '{task}' at {reminder_time}")

        # Translate text
        elif 'translate' in query:
            speak("What do you want me to translate?")
            sentence = take_user_input()
            speak("Which language do you want to translate to?")
            language = take_user_input()
            translation = translate_text(sentence, language)
            speak(f"The translation is: {translation}")
            print(translation)

        # Define word
        elif 'define' in query:
            speak("What word do you want me to define?")
            word = take_user_input()
            definition = get_word_definition(word)
            speak(f"The definition of {word} is: {definition}")
            print(definition)

# Function for the main loop
def main_loop():
    global previous_x, previous_y  # Declare as global to modify their values inside the loop
    greet_user()

    # Start the voice recognition in a separate thread
    voice_thread = threading.Thread(target=voice_recognition_thread)
    voice_thread.daemon = True  # This allows the thread to exit when the main program exits
    voice_thread.start()

    # Hand tracking and cursor control loop
    last_click_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a more intuitive experience
        frame_height, frame_width, _ = frame.shape
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wrist_x = wrist.x * frame_width
                wrist_y = wrist.y * frame_height
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Initialize previous_x and previous_y on first detection
                if previous_x is None or previous_y is None:
                    previous_x, previous_y = wrist_x, wrist_y  # Start with wrist as initial position

                # Check for pinch gesture (index and thumb together)
                if is_pinch(hand_landmarks, frame_width, frame_height):
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x = int(index_tip.x * frame_width)
                    y = int(index_tip.y * frame_height)

                    # Map the hand movement to virtual screen dimensions
                    virtual_screen_x = np.interp(x, [0, frame_width], [0, screen_width * scale_factor_x])
                    virtual_screen_y = np.interp(y, [0, frame_height], [0, screen_height * scale_factor_y])

                    # Smoothing the cursor movement
                    final_x = previous_x * smooth_factor + virtual_screen_x * (1 - smooth_factor)
                    final_y = previous_y * smooth_factor + virtual_screen_y * (1 - smooth_factor)

                    pyautogui.moveTo(final_x, final_y)
                    previous_x, previous_y = final_x, final_y
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                # Check for middle-thumb together (click gesture)
                elif is_middle_thumb_together(hand_landmarks, frame_width, frame_height):
                    current_time = time.time()
                    if current_time - last_click_time > 0.5:
                        if wrist_x < frame_width / 2:
                            pyautogui.click(button='right')
                        else:
                            pyautogui.click(button='left')
                        last_click_time = current_time

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the program
if __name__ == '__main__':
    main_loop()

