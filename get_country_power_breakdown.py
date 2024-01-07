import requests
import streamlit as st


@st.cache_data
def get_country_power_breakdown():

    url = 'https://api-access.electricitymaps.com/'
    get_archives = 'free-tier/power-breakdown/latest?zone=TR'

    headers = {
        "auth-token": "K0ibQ9hdlcllUb0Um9pfqtbkbKKf0Rr1"
    }

    response = requests.get(url + get_archives, headers=headers)
    outputs = response.json()
    outputs = outputs['powerProductionBreakdown']

    return outputs


