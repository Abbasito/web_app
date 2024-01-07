import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Page setting

st.set_page_config(
    page_title="Electro Generation for Turkey",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This App is created by Abı. This APP graphs *electricity generation breakdown* and *carbon footprint* data!"}
)



def get_weather_data():
    url = 'https://weatherapi-com.p.rapidapi.com/current.json'

    headers = {"X-RapidAPI-Key": "2bc76f3170msh36ecfc3a0a619acp1d9976jsn1e63aae1a069",
               "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}

    querystring = {"q": "Istanbul"}
    #   "dt": "2023-12-16"
    response = requests.get(url, headers=headers, params=querystring)
    outputs = response.json()

    return outputs


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


# Data
data_json_weather = get_weather_data()
data_json_currency = get_currency_data()
data_json_emission = get_country_co2_emission()
data_json_power = get_country_power_breakdown()

# CURRENCY
eur = data_json_currency[0]
usd = data_json_currency[1]
azn = data_json_currency[2]

# WEATHER
city = data_json_weather['location']['name']
local_time = data_json_weather['location']['localtime']
temperature = data_json_weather['current']['temp_c']
weather = data_json_weather['current']['condition']['text']
wind_speed = data_json_weather['current']['wind_kph']
humidity = data_json_weather['current']['humidity']
precipitations = data_json_weather['current']['precip_mm']

# ENERGY GENEREATION

data_json_power = pd.DataFrame(list(data_json_power.items()), columns=['Source', 'Value'])
data_json_emission= pd.DataFrame(list(data_json_emission.items()), columns=['Time', 'Carbon emission in tons'])

#   PAGE LAYOUT
a1, a2 = st.columns([3, 2], gap='medium')

with a1:
    st.image('istanbul.png')
with a2:
    st.header('Weather in Istanbul')
    st.metric("Temperature, C", temperature)
    st.metric("Wind, km/h", wind_speed)
    st.metric("Humidity, %", humidity)

mid = st.columns(1)
st.header('International Currencies')

b1, b2, b3, b4 = st.columns([2, 2, 2, 2], gap='medium')

with b1:
    st.subheader('1 Euro = ')
    st.metric('TRY', eur)

with b2:
    st.subheader('1 USD = ')
    st.metric('TRY', usd)

with b3:
    st.subheader('1 AZN = ')
    st.metric('TRY', azn)

c1, c2 = st.columns(2)

with c1:
    fig = px.pie(data_json_power, values='Value', names='Source', title='Energy Source Distribution')
    st.plotly_chart(fig)


with c2:
    fig = px.line(data_json_emission, x='Time', y='Carbon emission in tons', title='Latest Carbon Emission')
    fig.update_layout(
        plot_bgcolor='#8b9da8',
        xaxis=dict(showgrid=False),

    )
    fig.update_traces(line=dict(color='blue', width=2))
    st.plotly_chart(fig)

