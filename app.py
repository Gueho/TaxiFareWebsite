import datetime
import streamlit as st
import requests
import pandas as pd

'''
# Taxi Fare Predictor
'''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:'''


date = st.date_input('date')
time = st.time_input('time')
date_time = datetime.datetime.combine(date, time)
pickup_address = st.text_input('pickup address', value = 'Central Park')
dropoff_address = st.text_input('dropoff address', value = 'JFK')
passenger_count = st.number_input('passenger count', min_value = 1, max_value = 8)

if st.button('Calculate'):
    pickuploc_params = {
        'q': pickup_address,
        'format': 'json'
    }
    dropoffloc_params = {
        'q': dropoff_address,
        'format': 'json'
    }
    geo_url = "https://nominatim.openstreetmap.org"
    pickup_response = requests.get(geo_url, params = pickuploc_params).json()
    dropoff_response = requests.get(geo_url, params = dropoffloc_params).json()


pickup_latitude = float(pickup_response[0]['lat'])
pickup_longitude = float(pickup_response[0]['lon'])
dropoff_latitude = float(dropoff_response[0]['lat'])
dropoff_longitude = float(dropoff_response[0]['lon'])

# pickup_longitude = st.number_input('pickup address')
# pickup_latitude = st.number_input('pickup latitude')
# dropoff_longitude = st.number_input('dropoff longitude')
# dropoff_latitude = st.number_input('dropoff latitude')
#

loc_dict = {'lat': [pickup_latitude, dropoff_latitude],
              'lon': [pickup_longitude, dropoff_longitude]}


loc_df = pd.DataFrame.from_dict(loc_dict)

pickup_loc = loc_df.iloc[[0]]
dropoff_loc = loc_df.iloc[[1]]



# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...
# '''
params = dict(pickup_datetime = [date_time],
            pickup_longitude = [pickup_longitude],
            pickup_latitude = [pickup_latitude],
            dropoff_longitude = [dropoff_longitude],
            dropoff_latitude = [dropoff_latitude],
            passenger_count = [int(passenger_count)])
# '''

# 3. Let's call our API using the `requests` package...'''
response = requests.get(url, params = params).json()

# '''
# 4. Let's retrieve the prediction from the **JSON** returned by the API...
# st.metric(label, value, delta=None, delta_color="normal")
# ## Finally, we can display the prediction to the user
# '''
fare = round(response['fare'], 2)
st.metric('Expected:', f'{fare}$', delta=None, delta_color="normal")
st.map(loc_df)
