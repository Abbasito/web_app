import requests
import streamlit as st
import pandas as pd
import plotly.express as px

from get_weather_data import get_weather_data
from get_currency_data import get_currency_data
from get_country_power_breakdown import get_country_power_breakdown
from get_country_co2_emission import get_country_co2_emission

# Page setting

st.set_page_config(
    page_title="Electro Generation for Turkey",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This App is created by Abı. This APP graphs *electricity generation breakdown* and *carbon footprint* data!"}
)

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

