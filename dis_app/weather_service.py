import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude, forecast_days=7):

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "cloud_cover,"
            "pressure_msl,"
            "wind_speed_10m,"
            "weather_code"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "rain_sum,"
            "wind_speed_10m_max,"
            "weather_code"
        ),

        "forecast_days": forecast_days,
        "timezone": "auto"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# WEATHER CODE DESCRIPTION
# --------------------------------------------------

def weather_description(weather_code):

    weather_codes = {

        0: "Clear Sky",

        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing Rime Fog",

        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Heavy Drizzle",

        56: "Light Freezing Drizzle",
        57: "Heavy Freezing Drizzle",

        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",

        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",

        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",

        77: "Snow Grains",

        80: "Light Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",

        85: "Light Snow Showers",
        86: "Heavy Snow Showers",

        95: "Thunderstorm",

        96: "Thunderstorm with Light Hail",
        99: "Thunderstorm with Heavy Hail",
    }

    return weather_codes.get(
        weather_code,
        "Unknown Weather"
    )


# --------------------------------------------------
# RISK CALCULATION
# --------------------------------------------------

def calculate_risk(current_weather):

    if not current_weather:
        return {
            "level": "UNKNOWN",
            "reason": "Weather information is unavailable.",
            "recommendation": "Please try again later."
        }

    rainfall = current_weather.get(
        "precipitation",
        0
    ) or 0

    wind_speed = current_weather.get(
        "wind_speed_10m",
        0
    ) or 0

    weather_code = current_weather.get(
        "weather_code"
    )

    # HIGH RISK

    if rainfall >= 50:

        return {
            "level": "HIGH",
            "reason": "Heavy rainfall detected.",
            "recommendation": (
                "Avoid low-lying areas and "
                "follow local disaster-management "
                "announcements."
            )
        }

    if wind_speed >= 50:

        return {
            "level": "HIGH",
            "reason": "Very high wind speed detected.",
            "recommendation": (
                "Avoid exposed areas and "
                "stay indoors if possible."
            )
        }

    if weather_code in [95, 96, 99]:

        return {
            "level": "HIGH",
            "reason": "Thunderstorm conditions detected.",
            "recommendation": (
                "Stay indoors and avoid open areas "
                "during the thunderstorm."
            )
        }

    # MEDIUM RISK

    if rainfall >= 20:

        return {
            "level": "MEDIUM",
            "reason": "Moderate to heavy rainfall detected.",
            "recommendation": (
                "Stay alert for waterlogging and "
                "possible local flooding."
            )
        }

    if wind_speed >= 30:

        return {
            "level": "MEDIUM",
            "reason": "Strong winds detected.",
            "recommendation": (
                "Avoid unnecessary travel and "
                "secure loose outdoor objects."
            )
        }

    if weather_code in [
        61,
        63,
        65,
        80,
        81,
        82
    ]:

        return {
            "level": "MEDIUM",
            "reason": "Rainfall conditions detected.",
            "recommendation": (
                "Carry necessary rain protection "
                "and stay alert for changing weather."
            )
        }

    # LOW RISK

    return {
        "level": "LOW",
        "reason": "No significant weather risk detected.",
        "recommendation": (
            "Normal activities can continue "
            "while monitoring weather updates."
        )
    }

def calculate_forecast_risk(forecast):

    if not forecast:
        return {
            "level": "UNKNOWN",
            "type": "Unknown",
            "reason": "Forecast information is unavailable.",
            "recommendation": "Please try again later."
        }

    highest_risk = "LOW"
    risk_type = "Normal Weather"
    reason = "No significant weather risk is expected."
    recommendation = (
        "Continue normal activities while "
        "monitoring weather updates."
    )

    risk_priority = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    for day in forecast:

        rainfall = day.get(
            "precipitation",
            0
        ) or 0

        wind_speed = day.get(
            "max_wind_speed",
            0
        ) or 0

        weather_code = day.get(
            "weather_code"
        )

        # -----------------------------
        # HIGH RISK
        # -----------------------------

        if rainfall >= 50:

            current_risk = "HIGH"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Heavy Rainfall"

                reason = (
                    f"Heavy rainfall is expected on "
                    f"{day.get('date')}."
                )

                recommendation = (
                    "Avoid low-lying and flood-prone "
                    "areas and follow official "
                    "disaster-management instructions."
                )

        elif wind_speed >= 50:

            current_risk = "HIGH"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Strong Wind"

                reason = (
                    f"Very strong winds are expected on "
                    f"{day.get('date')}."
                )

                recommendation = (
                    "Avoid exposed areas and secure "
                    "loose outdoor objects."
                )

        elif weather_code in [95, 96, 99]:

            current_risk = "HIGH"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Thunderstorm"

                reason = (
                    f"Thunderstorm conditions are "
                    f"expected on {day.get('date')}."
                )

                recommendation = (
                    "Stay indoors during thunderstorms "
                    "and avoid open areas."
                )

        # -----------------------------
        # MEDIUM RISK
        # -----------------------------

        elif rainfall >= 20:

            current_risk = "MEDIUM"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Heavy Rain"

                reason = (
                    f"Significant rainfall is expected "
                    f"on {day.get('date')}."
                )

                recommendation = (
                    "Stay alert for waterlogging and "
                    "possible local flooding."
                )

        elif wind_speed >= 30:

            current_risk = "MEDIUM"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Strong Wind"

                reason = (
                    f"Strong winds are expected on "
                    f"{day.get('date')}."
                )

                recommendation = (
                    "Avoid unnecessary travel and "
                    "secure loose objects."
                )

        elif weather_code in [
            61,
            63,
            65,
            80,
            81,
            82
        ]:

            current_risk = "MEDIUM"

            if risk_priority[current_risk] > risk_priority[highest_risk]:

                highest_risk = current_risk

                risk_type = "Rain"

                reason = (
                    f"Rainfall is expected on "
                    f"{day.get('date')}."
                )

                recommendation = (
                    "Carry rain protection and "
                    "monitor changing weather conditions."
                )

    return {
        "level": highest_risk,
        "type": risk_type,
        "reason": reason,
        "recommendation": recommendation
    }
# --------------------------------------------------
# FORMAT CURRENT WEATHER
# --------------------------------------------------

def get_current_weather(weather_data):

    current = weather_data.get(
        "current",
        {}
    )

    weather_code = current.get(
        "weather_code"
    )

    return {

        "time": current.get(
            "time"
        ),

        "temperature": current.get(
            "temperature_2m"
        ),

        "humidity": current.get(
            "relative_humidity_2m"
        ),

        "precipitation": current.get(
            "precipitation"
        ),

        "rain": current.get(
            "rain"
        ),

        "cloud_cover": current.get(
            "cloud_cover"
        ),

        "pressure": current.get(
            "pressure_msl"
        ),

        "wind_speed": current.get(
            "wind_speed_10m"
        ),

        "weather_code": weather_code,

        "weather": weather_description(
            weather_code
        )
    }


# --------------------------------------------------
# FORMAT DAILY FORECAST
# --------------------------------------------------

def get_daily_forecast(weather_data):

    daily = weather_data.get(
        "daily",
        {}
    )

    dates = daily.get(
        "time",
        []
    )

    max_temperatures = daily.get(
        "temperature_2m_max",
        []
    )

    min_temperatures = daily.get(
        "temperature_2m_min",
        []
    )

    precipitation = daily.get(
        "precipitation_sum",
        []
    )

    rain = daily.get(
        "rain_sum",
        []
    )

    wind = daily.get(
        "wind_speed_10m_max",
        []
    )

    weather_codes = daily.get(
        "weather_code",
        []
    )

    forecast = []

    for i in range(len(dates)):

        code = weather_codes[i]

        forecast.append({

            "date": dates[i],

            "max_temperature": (
                max_temperatures[i]
            ),

            "min_temperature": (
                min_temperatures[i]
            ),

            "precipitation": (
                precipitation[i]
            ),

            "rain": (
                rain[i]
            ),

            "max_wind_speed": (
                wind[i]
            ),

            "weather_code": code,

            "weather": weather_description(
                code
            )
        })

    return forecast

def calculate_overall_risk(current_risk, forecast_risk):

    risk_priority = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    current_level = current_risk.get(
        "level",
        "UNKNOWN"
    )

    forecast_level = forecast_risk.get(
        "level",
        "UNKNOWN"
    )

    # If either risk is HIGH
    if (
        current_level == "HIGH"
        or forecast_level == "HIGH"
    ):
        if current_level == "HIGH":
            selected_risk = current_risk
        else:
            selected_risk = forecast_risk

        return {
            "level": "HIGH",
            "type": selected_risk.get(
                "type",
                "Severe Weather"
            ),
            "reason": selected_risk.get(
                "reason"
            ),
            "recommendation": selected_risk.get(
                "recommendation"
            )
        }

    # If either risk is MEDIUM
    if (
        current_level == "MEDIUM"
        or forecast_level == "MEDIUM"
    ):
        if current_level == "MEDIUM":
            selected_risk = current_risk
        else:
            selected_risk = forecast_risk

        return {
            "level": "MEDIUM",
            "type": selected_risk.get(
                "type",
                "Weather Risk"
            ),
            "reason": selected_risk.get(
                "reason"
            ),
            "recommendation": selected_risk.get(
                "recommendation"
            )
        }

    # Both LOW
    return {
        "level": "LOW",
        "type": "Normal Weather",
        "reason": (
            "No significant current or "
            "forecast weather risk detected."
        ),
        "recommendation": (
            "Normal activities can continue "
            "while monitoring weather updates."
        )
    }