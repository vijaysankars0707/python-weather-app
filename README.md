# Task 4 - Weather App

## Setup
Create a free OpenWeatherMap API key and set it as an environment variable.

### Windows PowerShell
```powershell
$env:OPENWEATHER_API_KEY="your_api_key"
python -m pip install -r requirements.txt
python weather_app.py
```

### Linux/macOS
```bash
export OPENWEATHER_API_KEY="your_api_key"
python -m pip install -r requirements.txt
python weather_app.py
```

## Features
- City input validation
- Current temperature in Celsius and Fahrenheit
- Humidity
- Weather condition
- Wind speed
- Error handling for missing/invalid API keys, unknown cities, timeouts and network errors
- Approximately next 6 forecast entries
- Five-day overview derived from the standard forecast response

## API note
The app deliberately reads the API key from an environment variable rather than hard-coding it. Do not publish your key in GitHub or screenshots.

The forecast endpoint used here provides 3-hour forecast entries, so the "hourly" panel represents the next available forecast entries rather than six exact one-hour observations.
