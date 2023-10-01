from src.function.weather import get_weather


def form_weather(city_name):
    message = ""
    forecast = get_weather(city_name)
    if forecast:
        message = f"Forecast for {forecast['city']}, {forecast['country']}:\n\n"
        for period in forecast["periods"]:
            message += f"{period['timestamp'].strftime('%d %b %H:%M')}\n"
            message += f"Temperature: {period['temp']}°C\n"
            message += f"Description: {period['description']}\n\n"
    return message
