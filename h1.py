import requests
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
import subprocess
import json 
import openai

# Weather API key
WEATHER_API_KEY = "07de3d64c8ce42da991120909240106"
# OpenAI API key
OPENAI_API_KEY = "sk-proj-2epRZjZLxIiEJUiy0TMJT3BlbkFJEs9w6tQJkvhJwUeOoVfy"

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

def get_current_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes"
    try:
        r = requests.get(url)
        r.raise_for_status()
        weather_data = r.json()

        current_temp = weather_data["current"]["temp_c"]
        condition = weather_data["current"]["condition"]["text"]
        wind_speed = weather_data["current"]["wind_kph"]
        air_quality = weather_data["current"]["air_quality"].get("us-epa-index", "N/A")
        humidity = weather_data["current"]["humidity"]
        is_raining = 'rain' in condition.lower()
        rain_probability = weather_data["current"].get("precip_mm", 0)

        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%A, %B %d, %Y")

        return current_temp, condition, wind_speed, air_quality, humidity, is_raining, rain_probability, current_time, current_date
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None, None, None, None, None, None, None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None, None, None, None, None, None, None, None, None

def get_weekly_forecast(city):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=7&aqi=yes"
    try:
        r = requests.get(url)
        r.raise_for_status()
        forecast_data = r.json()

        forecast_days = forecast_data["forecast"]["forecastday"]
        weekly_forecast = []

        for day in forecast_days:
            date_str = day["date"]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            condition = day["day"]["condition"]["text"]
            wind_speed = day["day"]["maxwind_kph"]
            air_quality = day["day"].get("air_quality", {}).get("us-epa-index", "N/A")
            humidity = day["day"]["avghumidity"]
            chance_of_rain = day["day"]["daily_chance_of_rain"]

            weekly_forecast.append({
                "day_name": day_name,
                "date": date_str,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "condition": condition,
                "wind_speed": wind_speed,
                "air_quality": air_quality,
                "humidity": humidity,
                "rain_probability": chance_of_rain
            })

        return weekly_forecast
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def get_hourly_forecast(city):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&hours=24&aqi=yes"
    try:
        r = requests.get(url)
        r.raise_for_status()
        forecast_data = r.json()

        forecast_hours = forecast_data["forecast"]["forecastday"][0]["hour"]
        hourly_forecast = []
        for hour in forecast_hours:
            time_str = hour["time"]
            date_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            time_formatted = date_obj.strftime('%I %p')
            temp = hour["temp_c"]
            condition = hour["condition"]["text"]
            wind_speed = hour["wind_kph"]
            humidity = hour["humidity"]
            air_quality = hour.get("air_quality", {}).get("us-epa-index", "N/A")
            rain_probability = hour.get("chance_of_rain", 0)

            hourly_forecast.append({
                "time": time_formatted,
                "temp": temp,
                "condition": condition,
                "wind_speed": wind_speed,
                "humidity": humidity,
                "air_quality": air_quality,
                "rain_probability": rain_probability
            })
        return hourly_forecast
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def initialize_tts_engine():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 175)
        return engine
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        return None

def jarvis_speak(engine, text_to_speak):
    try:
        print(f"Jarvis: {text_to_speak}")
        engine.say(text_to_speak)
        engine.runAndWait()
    except Exception as e:
        print(f"Error while speaking: {e}")

def jarvis_greeting():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def jarvis_listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10)  # Set timeout to 10 seconds
            print("Processing audio...")
            command = recognizer.recognize_google(audio).lower()
            print(f"You: {command}")
            return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except sr.WaitTimeoutError:
        print("Listening timed out. Please try again.")
        return ""
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return ""

def calculate_feels_like_temperature(temp_c, wind_kph, humidity):
    if temp_c < 10 and wind_kph > 4.8:
        wind_chill = 13.12 + 0.6215 * temp_c - 11.37 * (wind_kph ** 0.16) + 0.3965 * temp_c * (wind_kph ** 0.16)
    else:
        wind_chill = temp_c

    feels_like_temp = wind_chill + (0.33 * humidity) - 0.70 * wind_kph - 4.00
    
    return round(feels_like_temp, 1)

def open_website(url):
    try:
        webbrowser.open(url)
        print(f"Opening {url}")
    except Exception as e:
        print(f"Error opening {url}: {e}")

def open_vs_code():
    try:
        # This assumes the 'code' command is available in your system PATH
        subprocess.run(["code"], check=True)
        print("Opening Visual Studio Code")
    except Exception as e:
        print(f"Error opening VS Code: {e}")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for the latest model
            messages=[
                {"role": "user","content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response at the moment."

if __name__ == "__main__":
    engine = initialize_tts_engine()

    print(jarvis_greeting())

    while True:
        jarvis_speak(engine, "What would you like to do? You can ask for weather updates, open browser, chat or exit.")
        command = jarvis_listen().strip()

        if "weather update" in command:
            jarvis_speak(engine, "Which city's weather would you like to check?")
            city = jarvis_listen().strip()

            if city:
                print(f"You: {city}")
                jarvis_speak(engine, f"Thank you! Fetching weather information for {city}.")
                current_temp, condition, wind_speed, air_quality, humidity, is_raining, rain_probability, current_time, current_date = get_current_weather(city)
                jarvis_speak(engine, "Would you like to check the current, weekly forecast, hourly forecast, or exit?")
                response = jarvis_listen()
                if response:
                    if "current" in response:
                        feels_like_temp = calculate_feels_like_temperature(current_temp, wind_speed, humidity)
                        weather_info = (f"Currently in {city}, on {current_date} at {current_time}, the temperature is {current_temp}°C with {condition}. "
                                        f"The wind speed is {wind_speed} kph, humidity is {humidity}%, "
                                        f"and the air quality index is {air_quality}. It feels like {feels_like_temp}°C."
                                        f"Chance of Rain: {rain_probability}%.")
                        if is_raining:
                            weather_info += f" It is raining with a probability of {rain_probability}%."
                        jarvis_speak(engine, weather_info)
                    elif "weekly" in response:
                        weekly_forecast = get_weekly_forecast(city)
                        if weekly_forecast:
                            for day in weekly_forecast:
                                forecast_info = (f"{day['day_name']}, {day['date']}: Max Temp: {day['max_temp']}°C, "
                                                f"Min Temp: {day['min_temp']}°C, Condition: {day['condition']}, "
                                                f"Wind Speed: {day['wind_speed']} kph, Humidity: {day['humidity']}%, "
                                                f"Air Quality Index: {day['air_quality']}, Chance of Rain: {day['rain_probability']}%.")
                                jarvis_speak(engine, forecast_info)
                        else:
                            jarvis_speak(engine, "Sorry, I couldn't fetch the weekly forecast information at the moment.")
                    elif "hourly" in response:
                        hourly_forecast = get_hourly_forecast(city)
                        if hourly_forecast:
                            for hour in hourly_forecast:
                                forecast_info = (f"At {hour['time']}, the temperature will be {hour['temp']}°C with {hour['condition']}. "
                                                f"Wind Speed: {hour['wind_speed']} kph, Humidity: {hour['humidity']}%, "
                                                f"Air Quality Index: {hour['air_quality']}, Chance of Rain: {hour['rain_probability']}%.")
                                jarvis_speak(engine, forecast_info)
                        else:
                            jarvis_speak(engine, "Sorry, I couldn't fetch the hourly forecast information at the moment.")
                    elif "exit" in response:
                        jarvis_speak(engine, "Alright, have a good day!")
                        break
                    else:
                        jarvis_speak(engine, "Sorry, I didn't understand that request.")
        elif "open browser" in command:
            jarvis_speak(engine, "Which browser would you like to open?")
            browser = jarvis_listen().strip()
            if "chrome" in browser.lower():
                open_website("https://www.google.com/chrome/")
            elif "firefox" in browser.lower():
              open_website("https://www.mozilla.org/firefox/")
            elif "safari" in browser.lower():
                 open_website("https://www.apple.com/safari/")
            elif "edge" in browser.lower():
                 open_website("https://www.microsoft.com/edge/")
            elif "youtube" in browser.lower():
                   open_website("https://www.youtube.com/")
            else:
                jarvis_speak(engine, "Sorry, I don't recognize that browser.")
        elif "chat" in command:
            jarvis_speak(engine, "What would you like to chat about?") 
            user_input = jarvis_listen().strip()
            if user_input:
                response = generate_response(user_input)
                jarvis_speak(engine, response)
        elif "open vs code" in command:
            open_vs_code()
        elif "exit" in command:
            jarvis_speak(engine, "Alright, have a good day!")
            break
        else:
            jarvis_speak(engine, "Sorry, I didn't understand that request.")