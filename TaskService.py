import pandas as pd
import xlrd

import Constants
from Utils import xy_to_latlon

file_name = 'Mobilenote.xls'
sheet = 'Huolto'

def get_x_coordinates_from_file():
    workbook = xlrd.open_workbook('Mobilenote.xls')

    worksheet = workbook.sheet_by_name('Huolto')
    array = worksheet.col_values(35)#geometria x
    array.pop(0)
    return array

def get_y_coordinates_from_file():
    workbook = xlrd.open_workbook('Mobilenote.xls')

    worksheet = workbook.sheet_by_name('Huolto')
    array = worksheet.col_values(36)  # geometria y
    array.pop(0)
    return array

def get_types_from_file():
    workbook = xlrd.open_workbook('Mobilenote.xls')

    worksheet = workbook.sheet_by_name('Huolto')
    array = worksheet.col_values(1)  # Työn kuvaus
    array.pop(0)
    return array


def get_demand_from_types(tasks_types):
    array = []
    for i in tasks_types:
        if i == 'Rumputarkastus 1v':
            array.append(Constants.RUMPUTARKASTUS_1V)
        elif i == 'Siltatarkastus 1v':
            array.append(Constants.SILTATARKASTUS_1V)
        elif i == 'Vaihde 2v huolto':
            array.append(Constants.VAIHDE_2V_HUOLTO)
        elif i == 'Opastinhuolto 12kk':
            array.append(Constants.OPASTINHUOLTO_12KK)
        elif i == 'Akselinlaskijahuolto 12 kk':
            array.append(Constants.AKSELINLASKIJAHUOLTO_12KK)
        elif i == 'Kävelytarkastus 1 v kevät':
            array.append(Constants.KAVELYTARKASTUS_1V_KEVAT)
        elif i == 'Vaihde 2v huolto':
            array.append(Constants.VAIHDE_2V_HUOLTO)
        elif i == 'Kaapit ja kojut 12kk':
            array.append(Constants.KAAPIT_JA_KOJUT_12KK)
        elif i == 'Liikennepaikkatarkastus 1v':
            array.append(Constants.LIIKENNEPAIKKATARKASTUS_1V)

    return array

def create_node_coordinates(task_count):
    # set depot latitude and longitude
    depot_1_latitude = 60.2031430359331
    depot_1_longitude = 24.831880137248284

    depot_2_latitude = 60.18949602985186
    depot_2_longitude = 24.917047352139903

    tasks_x = get_x_coordinates_from_file()
    tasks_y = get_y_coordinates_from_file()
    tasks_types = get_types_from_file()
    tasks_demand = get_demand_from_types(tasks_types)
    tasks_demand = tasks_demand[0:task_count]
    tasks_demand.insert(0, 0)
    tasks_demand.insert(1, 0)

    tasks_xy = xy_to_latlon(tasks_x, tasks_y)
    x_coords = tasks_xy[1][0:task_count]
    # add depot as first
    x_coords.insert(0, depot_1_latitude)
    x_coords.insert(1, depot_2_latitude)
    y_coords = tasks_xy[0][0:task_count]
    y_coords.insert(0, depot_1_longitude)
    y_coords.insert(1, depot_2_longitude)

    return (x_coords, y_coords, tasks_demand)