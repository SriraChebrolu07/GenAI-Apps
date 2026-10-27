import streamlit as st
import requests

# Function to fetch weather data from OpenWeatherMap API
def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # You can change this to 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return data

# Streamlit app
def main():
    st.title("Weather App")

    # Get user input (city name)
    city = st.text_input("Enter city name:", "London")

    # Get OpenWeatherMap API key from the user
    api_key = st.text_input("Enter your OpenWeatherMap API key:")

    # Check if the user has entered an API key
    if not api_key:
        st.warning("Please enter your OpenWeatherMap API key.")
        st.stop()

    # Check if the user has entered a city name
    if not city:
        st.warning("Please enter a city name.")
        st.stop()

    # Fetch weather data
    weather_data = get_weather(api_key, city)

    # Display weather information
    if 'main' in weather_data:
        st.subheader(f"Weather in {city}")
        st.write(f"Temperature: {weather_data['main']['temp']}°C")
        st.write(f"Description: {weather_data['weather'][0]['description']}")
    else:
        st.warning("Error fetching weather data. Please check your input and API key.")

if __name__ == "__main__":
    main()
