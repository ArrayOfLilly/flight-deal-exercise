from datetime import datetime, timedelta
from pprint import pprint

import data_manager as dm
import flight_search as fs
import notification_manager as nm

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.

# 4. Pass the data back to the main.py file, so that you can print the data from main.py

data_manager = dm.DataManager()
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)

#  5. In main.py check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one
#  to the FlightSearch class to get the corresponding IATA code
#  for that city using the Flight Search API.
#  You should use the code you get back to update the sheet_data dictionary.
for row in sheet_data:
    try:
        if row['iataCode'] == '':
            flight_search = fs.FlightSearch()
            row['iataCode'] = flight_search.get_city_iata_code(row['city'])
    except KeyError:
        flight_search = fs.FlightSearch()
        row['iataCode'] = flight_search.get_city_iata_code(row['city'])
    else:
        pass
# pprint(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# Set search conditions for finding lowest price
flight_search = fs.FlightSearch()

# Origin city
from_city = input(f"Where would you like departure from?\n ")
from_city_iata_code = flight_search.get_city_iata_code(from_city)
# print(from_city)
print(from_city_iata_code)

# Currency
currency = input(f"Which currency would you like pay in?\n ")
for row in sheet_data:
    try:
        if row['currency'] != currency:
            row['currency'] = currency
            row['lowestPrice'] = 0
    except KeyError:
        row['currency'] = currency
        row['lowestPrice'] = 0
    else:
        pass
data_manager.update_currency()
# print('Done')

# Search interval
departure_date_from = datetime.today().date() + timedelta(days=1)
# print(departure_date_from)
six_month = 6 * 30
departure_date_to = departure_date_from + timedelta(days=six_month)
# print(departure_date_to)

for row in sheet_data:
    try:
        if row['lowestPrice'] == 0:
            row['lowestPrice'] = \
                flight_search.get_lowest_price(from_city_iata_code, row['iataCode'], departure_date_from,
                                               departure_date_to, currency).price[0]
        if row['lowestPrice'] > flight_search.get_lowest_price(from_city_iata_code, row['iataCode'], departure_date_from,
                                                               departure_date_to, currency).price[0]:
            row['lowestPrice'] = \
                flight_search.get_lowest_price(from_city_iata_code, row['iataCode'], departure_date_from,
                                               departure_date_to, currency).price[0]

            flight = flight_search.get_lowest_price(from_city_iata_code, row['iataCode'], departure_date_from,
                                                    departure_date_to, currency)

            body = (f"Only {flight.price[0]} {flight.currency[0]} to fly from {flight.origin_city[0]}-"
                    f"{flight.origin_airport[0]} to {flight.destination_city[0]}-{flight.destination_airport[0]}, "
                    f"from {flight.out_date[0]} to {flight.return_date}.")
            msg = f"Subject: Low price ALERT!!!\n\n {body}"

            notification_manager = nm.NotificationManager()
            notification_manager.send_notification_email(msg)

        print(f"Lowest price is: {row['lowestPrice']}")
    except IndexError:
        row['lowestPrice'] = 0
        print(f"Lowest price is: {row['lowestPrice']}")
    except KeyError:
        row['lowestPrice'] = flight_search.get_lowest_price(from_city_iata_code, row['iataCode'], departure_date_from,
                                                            departure_date_to, currency).price[0]
        print(f"Lowest price is: {row['lowestPrice']}")

data_manager.destination_data = sheet_data
data_manager.update_price()
