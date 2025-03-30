import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config  # Import config from decouple

# Function to find the public IP address
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

# Function to search Wikipedia
def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

# Function to play a video on YouTube
def play_on_youtube(video):
    kit.playonyt(video)

# Function to search on Google
def search_on_google(query):
    kit.search(query)

# Function to send a WhatsApp message
def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+420{number}", message)

# Fetch email details from environment variables
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

# Function to send an email
def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

# Function to get the latest news headlines
def get_latest_news():
    NEWS_API_KEY = config("NEWS_API_KEY")
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

# Function to get the trending movies
def get_trending_movies():
    TMDB_API_KEY = config("TMDB_API_KEY")
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

# Function to get a random joke
def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

# Function to get a random advice
def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

# Function to get the weather report for a city
def get_weather(city):
    API_KEY = config("OPENWEATHER_API_KEY")
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric").json()
    weather = response["weather"][0]["description"]
    temperature = response["main"]["temp"]
    feels_like = response["main"]["feels_like"]
    return weather, temperature, feels_like
