import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from functions.online_ops import (
    find_my_ip, get_random_advice, get_random_joke, 
    play_on_youtube, search_on_google, search_on_wikipedia, 
    send_email, send_whatsapp_message)
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from decouple import config
import threading


pyautogui.FAILSAFE = False


USERNAME = config('USER')
BOTNAME = config('BOTNAME')
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)


previous_x, previous_y = None, None  
smooth_factor = 0.5 


scale_factor = 1.6  


def speak(text):
    engine.say(text)
    engine.runAndWait()


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


def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        return 'None'
    return query.lower()


def is_pinch(hand_landmarks, frame_width, frame_height):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    pinch_distance = math.hypot(
        (index_finger_tip.x - thumb_tip.x) * frame_width,
        (index_finger_tip.y - thumb_tip.y) * frame_height
    )
    return pinch_distance < 30


def is_middle_thumb_together(hand_landmarks, frame_width, frame_height):
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_thumb_distance = math.hypot(
        (middle_finger_tip.x - thumb_tip.x) * frame_width,
        (middle_finger_tip.y - thumb_tip.y) * frame_height
    )
    return middle_thumb_distance < 30


def voice_recognition_thread():
    while True:
        query = take_user_input()
        
        if 'hello' in query:
            speak('Hello! How can I help you?')
        
        
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

        
        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}')
            print(f'Your IP Address is {ip_address}')

        
        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia?')
            search_query = take_user_input()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            print(results) 

        
        elif 'youtube' in query:
            speak('What do you want to play on Youtube?')
            video = take_user_input()
            play_on_youtube(video)

     
        elif 'search on google' in query:
            speak('What do you want to search on Google?')
            g_query = take_user_input()
            search_on_google(g_query)

        
        elif "send whatsapp message" in query:
            speak('On what number should I send the message? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message?")
            message = take_user_input()
            send_whatsapp_message(number, message)
            speak("I've sent the message.")
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

def main_loop():
    global previous_x, previous_y  
    greet_user()

  
    voice_thread = threading.Thread(target=voice_recognition_thread)
    voice_thread.daemon = True  
    voice_thread.start()

    
    last_click_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)          frame_height, frame_width, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wrist_x = wrist.x * frame_width
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

          
                if previous_x is None or previous_y is None:
                    previous_x, previous_y = wrist_x, wrist.x * frame_height  

               
                if is_pinch(hand_landmarks, frame_width, frame_height):
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x = int(index_tip.x * frame_width)
                    y = int(index_tip.y * frame_height)
                    virtual_screen_x = np.interp(x, [0, frame_width], [0, screen_width])
                    virtual_screen_y = np.interp(y, [0, frame_height], [0, screen_height])

                    
                    final_x = previous_x * smooth_factor + virtual_screen_x * (1 - smooth_factor)
                    final_y = previous_y * smooth_factor + virtual_screen_y * (1 - smooth_factor)

                    pyautogui.moveTo(final_x, final_y)
                    previous_x, previous_y = final_x, final_y
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                
                elif is_middle_thumb_together(hand_landmarks, frame_width, frame_height):
                    current_time = time.time()
                    if current_time - last_click_time > 0.5:
                        if wrist_x < frame_width / 2:
                            pyautogui.rightClick()
                        else:
                            pyautogui.click()
                        last_click_time = current_time
                        time.sleep(0.2)

        cv2.imshow("Hand Cursor", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_loop()

