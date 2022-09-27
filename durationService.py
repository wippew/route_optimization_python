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




