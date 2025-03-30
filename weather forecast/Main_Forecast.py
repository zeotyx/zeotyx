import requests
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("400x600")
root.config(bg="#2c3e50")  


title_label = tk.Label(root, text="Weather Forecast", font=("Helvetica", 22, 'bold'), fg="#f39c12", bg="#2c3e50")
title_label.pack(pady=20)


length_label = tk.Label(root, text="Enter City To Forecast:", font=("Helvetica", 14), fg="white", bg="#2c3e50")
length_label.pack(pady=10)


City_entry = tk.Entry(root, fg="black", bg="white", font=("Helvetica", 14), relief="solid", bd=2)
City_entry.pack(pady=5, ipadx=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14), justify="left", fg="white", bg="#34495e", relief="solid", bd=3)
result_label.pack(pady=20, padx=10)

API_KEY = "38e6df07f012ff1331a6e05c8db59233"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

unit_var = tk.StringVar(root)
unit_var.set("metric")

def Get_Forecast():
    city = City_entry.get()
    unit = unit_var.get()
    
    if city == "":
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    
    params = {"q": city, "appid": API_KEY, "units": unit}
    
    result_label.config(text="Fetching weather data... Please wait.")
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        rain = data.get("rain", {}).get("1h", 0)
        
        weather_info = (
            f"City: {city_name}, {country}\n"
            f"Temperature: {temp}° ({'Feels like: ' + str(feels_like) + '°' if temp != feels_like else ''})\n"
            f"Condition: {condition.capitalize()}\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Humidity: {humidity}%\n"
            f"Rain (last hour): {rain} mm"
        )
        result_label.config(text=weather_info)
    else:
        messagebox.showerror("Error", f"Unable to fetch data for {city}. Please try again.")


def on_enter(e, button):
    button.config(width=21, height=2)  

def on_leave(e, button):
    button.config(width=20, height=2)  

Weather_button = tk.Button(root, text="Get Weather", command=Get_Forecast, width=20, height=2, font=("Helvetica", 14), bg="#1abc9c", fg="white", relief="solid", bd=2)

Weather_button.bind("<Enter>", lambda e, button=Weather_button: on_enter(e, button))
Weather_button.bind("<Leave>", lambda e, button=Weather_button: on_leave(e, button))

Weather_button.pack(pady=20)


def open_settings():
    
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x400")
    settings_window.config(bg="#34495e")

    
    settings_label = tk.Label(settings_window, text="Settings", font=("Helvetica", 18, 'bold'), fg="#f39c12", bg="#34495e")
    settings_label.pack(pady=20)

    
    unit_label = tk.Label(settings_window, text="Select Unit for Weather:", font=("Helvetica", 12), fg="white", bg="#34495e")
    unit_label.pack(pady=10)

    unit_var_in_settings = tk.StringVar(settings_window)
    unit_var_in_settings.set(unit_var.get())  # Set the default value based on the main window
    unit_menu_in_settings = tk.OptionMenu(settings_window, unit_var_in_settings, "metric", "imperial", "standard")
    unit_menu_in_settings.config(font=("Helvetica", 12), bg="#34495e", fg="white", width=15)
    unit_menu_in_settings.pack(pady=10)


    def save_settings():
        unit_var.set(unit_var_in_settings.get())  
        settings_window.destroy()

    save_button = tk.Button(settings_window, text="Save Settings", command=save_settings, width=20, height=2, font=("Helvetica", 12), bg="#1abc9c", fg="white", relief="solid", bd=2)

    
    save_button.bind("<Enter>", lambda e, button=save_button: on_enter(e, button))
    save_button.bind("<Leave>", lambda e, button=save_button: on_leave(e, button))

    save_button.pack(pady=20)

    settings_window.mainloop()


Settings_button = tk.Button(root, text="Settings", command=open_settings, width=20, height=2, font=("Helvetica", 14), bg="#e67e22", fg="white", relief="solid", bd=2)


Settings_button.bind("<Enter>", lambda e, button=Settings_button: on_enter(e, button))
Settings_button.bind("<Leave>", lambda e, button=Settings_button: on_leave(e, button))

Settings_button.pack(pady=10)

root.mainloop()
