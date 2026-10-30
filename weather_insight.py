"""
AI Data Insight Report from a Public Dataset
Beginner project: Chennai historical weather, calendar year 2025.

Run:
    pip install -r requirements.txt
    python weather_insight.py

The script downloads historical daily weather from Open-Meteo, saves a CSV,
creates three charts, and prints data-derived findings.
Internet connection is required for the first run.
"""
from pathlib import Path
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUTPUT = Path("weather_output")
OUTPUT.mkdir(exist_ok=True)

# Chennai, Tamil Nadu
LATITUDE = 13.0827
LONGITUDE = 80.2707
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

URL = "https://archive-api.open-meteo.com/v1/archive"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Kolkata",
}

def download_weather():
    """Download daily historical weather and return it as a DataFrame."""
    print("Downloading historical weather data...")
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if "daily" not in payload:
        raise ValueError(f"Weather data was not returned: {payload}")

    df = pd.DataFrame(payload["daily"])
    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "max_temp_c",
        "temperature_2m_min": "min_temp_c",
        "precipitation_sum": "precipitation_mm",
    })
    df["date"] = pd.to_datetime(df["date"])
    for column in ["max_temp_c", "min_temp_c", "precipitation_mm"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Basic cleaning: remove rows with no date and sort chronologically.
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    df.to_csv(OUTPUT / "chennai_weather_2025.csv", index=False)
    return df

def analyze_weather(df):
    """Print simple statistics and save monthly summaries."""
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["temperature_range_c"] = df["max_temp_c"] - df["min_temp_c"]

    monthly = df.groupby(["month", "month_name"], as_index=False).agg(
        avg_max_temp_c=("max_temp_c", "mean"),
        avg_min_temp_c=("min_temp_c", "mean"),
        total_precipitation_mm=("precipitation_mm", "sum"),
        rainy_days=("precipitation_mm", lambda s: int((s > 0).sum())),
    )
    monthly.to_csv(OUTPUT / "monthly_summary.csv", index=False)

    hottest = df.loc[df["max_temp_c"].idxmax()]
    wettest = df.loc[df["precipitation_mm"].idxmax()]
    rainiest_month = monthly.loc[monthly["total_precipitation_mm"].idxmax()]
    warmest_month = monthly.loc[monthly["avg_max_temp_c"].idxmax()]

    print("\n=== WEATHER INSIGHT REPORT: CHENNAI, 2025 ===")
    print(f"Daily records analysed: {len(df)}")
    print(f"Average daily maximum temperature: {df['max_temp_c'].mean():.1f} °C")
    print(f"Average daily minimum temperature: {df['min_temp_c'].mean():.1f} °C")
    print(f"Total recorded precipitation: {df['precipitation_mm'].sum():.1f} mm")
    print(f"Days with precipitation above 0 mm: {(df['precipitation_mm'] > 0).sum()}")
    print(f"Hottest recorded day: {hottest['date'].date()} ({hottest['max_temp_c']:.1f} °C)")
    print(f"Wettest recorded day: {wettest['date'].date()} ({wettest['precipitation_mm']:.1f} mm)")
    print(f"Month with highest total precipitation: {rainiest_month['month_name']} "
          f"({rainiest_month['total_precipitation_mm']:.1f} mm)")
    print(f"Month with highest average maximum temperature: {warmest_month['month_name']} "
          f"({warmest_month['avg_max_temp_c']:.1f} °C)")

    # Chart 1: daily maximum and minimum temperature
    plt.figure(figsize=(11, 5))
    plt.plot(df["date"], df["max_temp_c"], label="Daily maximum (°C)", linewidth=1)
    plt.plot(df["date"], df["min_temp_c"], label="Daily minimum (°C)", linewidth=1)
    plt.title("Chennai Daily Temperatures — 2025")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT / "daily_temperature.png", dpi=160)
    plt.close()

    # Chart 2: monthly average maximum temperature
    plt.figure(figsize=(9, 5))
    plt.bar(monthly["month_name"], monthly["avg_max_temp_c"])
    plt.title("Monthly Average Daily Maximum Temperature — 2025")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(OUTPUT / "monthly_temperature.png", dpi=160)
    plt.close()

    # Chart 3: monthly precipitation total
    plt.figure(figsize=(9, 5))
    plt.bar(monthly["month_name"], monthly["total_precipitation_mm"])
    plt.title("Monthly Total Precipitation — 2025")
    plt.xlabel("Month")
    plt.ylabel("Precipitation (mm)")
    plt.tight_layout()
    plt.savefig(OUTPUT / "monthly_precipitation.png", dpi=160)
    plt.close()

    # Simple AI-ready summary: use actual computed values, not invented claims.
    summary = f"""AI-ASSISTED WEATHER SUMMARY — CHENNAI, 2025

Dataset records: {len(df)}
Average daily maximum temperature: {df['max_temp_c'].mean():.1f} °C
Average daily minimum temperature: {df['min_temp_c'].mean():.1f} °C
Total precipitation: {df['precipitation_mm'].sum():.1f} mm
Precipitation days (> 0 mm): {(df['precipitation_mm'] > 0).sum()}
Hottest day: {hottest['date'].date()}, {hottest['max_temp_c']:.1f} °C
Wettest day: {wettest['date'].date()}, {wettest['precipitation_mm']:.1f} mm
Highest-precipitation month: {rainiest_month['month_name']}
Highest-average-maximum-temperature month: {warmest_month['month_name']}

AI prompt suggestion:
"Explain these calculated weather statistics in beginner-friendly language.
Do not add facts not present in the summary. Distinguish correlation from
causation, mention that one location and one year cannot establish a long-term
climate trend, and suggest practical follow-up questions."
"""
    (OUTPUT / "insight_summary.txt").write_text(summary, encoding="utf-8")
    print(f"\nFiles saved in: {OUTPUT.resolve()}")
    print("Open the PNG charts and CSV files to inspect the results.")

def main():
    try:
        weather = download_weather()
        analyze_weather(weather)
    except requests.RequestException as error:
        print("Could not download data. Check your internet connection and try again.")
        print(f"Details: {error}")
    except (ValueError, KeyError) as error:
        print(f"Could not process the returned dataset: {error}")

if __name__ == "__main__":
    main()
