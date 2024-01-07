import requests
import streamlit as st


@st.cache_data
def get_country_co2_emission():

    url = 'https://api-access.electricitymaps.com/'
    get_archives = 'free-tier/carbon-intensity/history?zone=TR'

    headers = {
        "auth-token": "K0ibQ9hdlcllUb0Um9pfqtbkbKKf0Rr1"
    }

    response = requests.get(url + get_archives, headers=headers)
    outputs = response.json()

    value_dict = {}
    for i in range(len(outputs['history'])):
        date = f"{outputs['history'][i]['datetime']}"
        carbon_value = outputs['history'][i]['carbonIntensity']
        value_dict[date] = carbon_value

    return value_dict



