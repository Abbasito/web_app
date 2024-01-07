import requests
import streamlit as st


@st.cache_data
def get_currency_data():
    url = 'https://exchange-rate-api1.p.rapidapi.com/latest'

    headers = {'X-RapidAPI-Key': '2bc76f3170msh36ecfc3a0a619acp1d9976jsn1e63aae1a069',
                'X-RapidAPI-Host': 'exchange-rate-api1.p.rapidapi.com'}  #   YYY

    params = {'base': 'TRY'}

    response = requests.get(url, headers=headers, params=params)
    outputs = response.json()
    eur = round(1 / outputs['rates']['EUR'], 3)
    usd = round(1 / outputs['rates']['USD'], 3)
    azn = round(1 / outputs['rates']['AZN'], 3)
    currency = [eur, usd, azn]

    return currency


