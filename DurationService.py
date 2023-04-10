import numpy as np
import googlemaps
import gmaps
import googlemaps
# importing the requests library
import requests

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




def get_travel_times_as_matrix(df):
    duration_result = np.zeros((len(df), len(df)))
    df['latitude-longitude'] = '0'
    for i in range(len(df)):
        df['latitude-longitude'].iloc[i] = str(df.latitude[i]) + ',' + str(df.longitude[i])

    for i in range(len(df)):
        for j in range(len(df)):
            # calculate distance of all pairs
            if duration_result[j][i] == 0:
                test = duration_result[j][i]
                waypoint0 = df['latitude-longitude'].iloc[i]
                waypoint1 = df['latitude-longitude'].iloc[j]
                duration_result[i][j] = get_one_here_location(waypoint0, waypoint1)
            else:
                duration_result[i][j] = duration_result[j][i]

    return duration_result


def get_one_here_location(waypoint0, waypoint1):
    # api-endpoint
    URL = "https://route.api.here.com/routing/7.2/calculateroute.json"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}
    PARAMS["waypoint0"] = waypoint0
    PARAMS["waypoint1"] = waypoint1
    PARAMS["mode"] = "fastest;car;traffic:disabled"
    PARAMS["app_id"] = ""
    PARAMS["app_code"] = ""

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.json()

    # get travel_time from data
    travel_time = data['response']['route'][0]['leg'][0]['travelTime']

    return travel_time


