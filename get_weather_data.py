import requests
import streamlit as st


@st.cache_data
def get_weather_data():
    url = 'https://weatherapi-com.p.rapidapi.com/current.json'

    headers = {"X-RapidAPI-Key": "2bc76f3170msh36ecfc3a0a619acp1d9976jsn1e63aae1a069",
               "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}

    querystring = {"q": "Istanbul"}
    #   "dt": "2023-12-16"
    response = requests.get(url, headers=headers, params=querystring)
    outputs = response.json()

    return outputs

