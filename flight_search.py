import datetime
import time
from datetime import date, datetime
from pprint import pprint
from time import mktime

import requests

import flight_data as fd

TEQUILA_API_KEY = 'YsHhX8RmCn9f1DSyPRq1kRK3uJ3AGufO'
TEQUILA_END_POINT = 'https://api.tequila.kiwi.com'
TEQUILA_LOCATIONS_PATH = '/locations/query'
TEQUILA_SEARCH_PATH = '/v2/search'


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    @staticmethod
    def get_city_iata_code(city: str):
        headers = {
            'apikey': TEQUILA_API_KEY
        }

        parameters = {
            'term': city,
            'location_types': 'city'
        }

        url = TEQUILA_END_POINT + TEQUILA_LOCATIONS_PATH

        response = requests.get(url=url, params=parameters, headers=headers)
        response.raise_for_status()

        code = response.json()['locations'][0]['code']
        # pprint(code)

        return code

    @staticmethod
    def get_lowest_price(origin_city_code: str, destination_city_code: str, from_time: date, to_time: date,
                         currency: str):
        headers = {
            'apikey': TEQUILA_API_KEY
        }

        parameters = {
            'fly_from': origin_city_code,
            'fly_to': destination_city_code,
            'date_from': from_time,
            'date_to': to_time,
            'nights_in_dst_from': 4,
            'nights_in_dst_to': 7,
            'one_for_city': 1,
            'curr': currency,
            'max_stopovers': 4,
            'max_sector_stopovers': 2,
            'sort': 'price',
            'limit': 1,
            'locale': 'en',
        }

        url = TEQUILA_END_POINT + TEQUILA_SEARCH_PATH

        response = requests.get(url=url, params=parameters, headers=headers)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
            # pprint(data)
        except IndexError:
            print("Didn't found a trip.")

            origin_city = '',
            origin_airport = '',
            destination_city = '',
            destination_airport = '',
            price = 0,
            currency = currency,
            out_date = '',
            return_date = ''

            flight_data = fd.FlightData(origin_city, origin_airport, destination_city, destination_airport, price,
                                        currency, out_date, return_date)
        else:
            # in case v1 API call
            # departure_time = datetime.fromtimestamp(mktime(time.localtime(data['route'][0]['dTime'])))
            # # print(departure_time)
            # arrival_time = datetime.fromtimestamp(mktime(time.localtime(data['route'][-1]['aTime'])))
            # # print(arrival_time)

            departure_time = data["route"][0]["local_departure"].split("T")[0]
            arrival_time = data["route"][-1]["local_arrival"].split("T")[0]

            origin_city = data["route"][0]["cityFrom"],
            origin_airport = data["route"][0]["flyFrom"],
            destination_city = data["route"][0]["cityTo"],
            destination_airport = data["route"][0]["flyTo"],
            price = round(data['price']),
            currency = currency,
            out_date = departure_time,
            return_date = arrival_time

            flight_data = fd.FlightData(origin_city, origin_airport, destination_city, destination_airport, price,
                                        currency, out_date, return_date)
            # print(f"{flight_data.destination_city}: {flight_data.price} {flight_data.currency}")
            print(f"{flight_data.destination_city[0]}: {flight_data.price[0]} {flight_data.currency[0]}")

            pprint(flight_data.__dict__)

        return flight_data
