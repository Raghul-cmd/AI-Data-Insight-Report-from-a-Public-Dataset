# AI Data Insight Report from a Public Dataset

## Project
Beginner-level Python analysis of historical daily weather in Chennai, Tamil Nadu, for 1 Jan–31 Dec 2025.

## Dataset
Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api  
The API provides daily maximum/minimum temperature and precipitation. The data is downloaded when the script runs.

## Setup (Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python weather_insight.py
```

## Output files
The script creates `weather_output/` containing:
- `chennai_weather_2025.csv` — daily data
- `monthly_summary.csv` — monthly aggregates
- `daily_temperature.png` — maximum/minimum temperature line chart
- `monthly_temperature.png` — monthly average maximum temperature bar chart
- `monthly_precipitation.png` — monthly precipitation bar chart
- `insight_summary.txt` — calculated results and a prompt for AI-assisted explanation

## Methodology
1. Request daily historical weather from the public API.
2. Convert dates and numeric columns to appropriate data types.
3. Remove rows without a date and sort by date.
4. Calculate average temperatures, total precipitation, precipitation days, hottest/wettest day, and monthly summaries.
5. Plot the results and save the outputs.
6. Optionally use an AI assistant to explain the calculated summary. Verify all numerical claims against the CSV.

## Limitations
This is one location and one year; it cannot prove climate change or establish long-term trends. Historical values are reanalysis/model-based estimates, not necessarily direct measurements from a station at the exact coordinates. API access requires internet. AI-generated explanations should be checked.
