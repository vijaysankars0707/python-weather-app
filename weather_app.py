import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def c_to_f(c):
    return c * 9 / 5 + 32


def get_weather():
    city = city_var.get().strip()
    if not city:
        show_error("Enter a city name.")
        return

    if not API_KEY:
        show_error("OPENWEATHER_API_KEY is not configured.")
        return

    try:
        current = requests.get(
            CURRENT_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
        current.raise_for_status()
        data = current.json()

        forecast = requests.get(
            FORECAST_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
        forecast.raise_for_status()
        forecast_data = forecast.json()

        display_current(data)
        display_forecast(forecast_data)

    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 401:
            show_error("Invalid API key.")
        elif exc.response is not None and exc.response.status_code == 404:
            show_error("City not found.")
        else:
            show_error("The weather service returned an error.")
    except requests.Timeout:
        show_error("The weather request timed out.")
    except requests.RequestException:
        show_error("Network error. Check your internet connection.")
    except (KeyError, ValueError):
        show_error("The weather service returned unexpected data.")


def show_error(message):
    error_var.set(message)
    current_var.set("")


def display_current(data):
    city = data.get("name", city_var.get())
    country = data.get("sys", {}).get("country", "")
    main = data["main"]
    weather = data["weather"][0]
    wind = data.get("wind", {}).get("speed", 0)

    temp = main["temp"]
    text = (
        f"{city}, {country}\n"
        f"{temp:.1f} °C / {c_to_f(temp):.1f} °F\n"
        f"{weather['description'].title()}\n"
        f"Humidity: {main['humidity']}%\n"
        f"Wind: {wind:.1f} m/s"
    )
    current_var.set(text)
    error_var.set("")


def display_forecast(data):
    forecast_box.delete(0, tk.END)

    # OpenWeather's standard forecast endpoint supplies 3-hour forecast entries.
    # The first six entries provide approximately the next 18 hours.
    for item in data.get("list", [])[:6]:
        timestamp = datetime.fromtimestamp(item["dt"]).strftime("%a %H:%M")
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"].title()
        forecast_box.insert(tk.END, f"{timestamp} | {temp:.1f} °C | {condition}")

    # Simple five-day view: one representative daytime entry per date.
    daily = {}
    for item in data.get("list", []):
        date = datetime.fromtimestamp(item["dt"]).date()
        daily.setdefault(date, item)

    daily_box.delete(0, tk.END)
    for date, item in list(daily.items())[:5]:
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"].title()
        daily_box.insert(tk.END, f"{date} | {temp:.1f} °C | {condition}")


root = tk.Tk()
root.title("Weather App")
root.geometry("700x650")
root.resizable(False, False)

main = ttk.Frame(root, padding=25)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Weather App", font=("Arial", 22, "bold")).pack(pady=(0, 15))

search = ttk.Frame(main)
search.pack(fill="x")
city_var = tk.StringVar()
ttk.Entry(search, textvariable=city_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
ttk.Button(search, text="Get Weather", command=get_weather).pack(side="right")

error_var = tk.StringVar()
ttk.Label(main, textvariable=error_var, foreground="red").pack(pady=8)

current_var = tk.StringVar(value="Enter a city and click Get Weather.")
ttk.Label(
    main, textvariable=current_var, justify="center",
    font=("Arial", 14), anchor="center"
).pack(fill="x", pady=15)

ttk.Label(main, text="Next forecast entries", font=("Arial", 12, "bold")).pack()
forecast_box = tk.Listbox(main, height=7)
forecast_box.pack(fill="x", pady=5)

ttk.Label(main, text="Five-day overview", font=("Arial", 12, "bold")).pack(pady=(15, 0))
daily_box = tk.Listbox(main, height=6)
daily_box.pack(fill="x", pady=5)

ttk.Label(
    main,
    text="Set OPENWEATHER_API_KEY before starting the application.",
).pack(pady=15)

root.mainloop()
