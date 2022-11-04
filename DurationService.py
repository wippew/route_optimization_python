import numpy as np
import googlemaps
import gmaps
import googlemaps

API_KEY = 'AIzaSyAUt4YSLzcTzqzujW20pA21ndsI1yeZOAY'
gmaps.configure(api_key=API_KEY)
googlemaps = googlemaps.Client(key=API_KEY)

# function for calculating distance between two pins
def duration_calculator(df):
    duration_result = np.zeros((len(df), len(df)))
    df['latitude-longitude'] = '0'
    for i in range(len(df)):
        df['latitude-longitude'].iloc[i] = str(df.latitude[i]) + ',' + str(df.longitude[i])

    for i in range(len(df)):
        for j in range(len(df)):
            # calculate distance of all pairs
            if duration_result[j][i] == 0:
                test2 = df['latitude-longitude'].iloc[i]
                test3 = df['latitude-longitude'].iloc[j]

                google_maps_api_result = googlemaps.directions(test2, test3, mode='driving')

                duration_result[i][j] = google_maps_api_result[0]['legs'][0]['duration']['value']
            else:
                duration_result[i][j] = duration_result[j][i]

    return duration_result


# importing the requests library
import requests


def get_here_locations():
    # api-endpoint
    URL = "https://route.api.here.com/routing/7.2/calculateroute.json"
#     asd = "https://route.api.here.com/routing/7.2/calculateroute.json?&mode=fastest%3Bcar%3Btraffic%3Aenabled&&app_id=CWt4Io2jWFGGLV9csUeX&app_code=ow1GDLeuAgI2yoDwidUKFw
#
    'https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0=60.1894%252C24.9170&waypoint1=60.1828%252C24.8318&mode=fastest%253Bcar%253Btraffic%253Aenabled%26&app_id=CWt4Io2jWFGGLV9csUeX&app_code=ow1GDLeuAgI2yoDwidUKFw'
    # location given here
    w0_long = "60.1894"
    w0_lat = "24.9170"

    w1_long = "60.1828"
    w1_lat = "24.8318"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}
    PARAMS["waypoint0"] = w0_long + "," + w0_lat
    PARAMS["waypoint1"] = w1_long + "," + w1_lat
    PARAMS["mode"] = "fastest;car;traffic:disabled"
    PARAMS["app_id"] = "CWt4Io2jWFGGLV9csUeX"
    PARAMS["app_code"] = "ow1GDLeuAgI2yoDwidUKFw"

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.json()

    # extracting latitude, longitude and formatted address
    # of the first matching location
    # latitude = data['results'][0]['geometry']['location']['lat']
    # longitude = data['results'][0]['geometry']['location']['lng']
    # formatted_address = data['results'][0]['formatted_address']

    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
          % (latitude, longitude, formatted_address))


