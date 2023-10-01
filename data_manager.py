import requests

SHEETY_API_ENDPOINT = "https://api.sheety.co/da7b4d88944f144200cb78f5ea94228d/flightDealsProject/prices"
AUTHORIZATION = 'Basic QXJyYXlPZkxpbGx5OlRtcF8xMjM0NQ=='


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        headers = {
            'Authorization': AUTHORIZATION,

        }

        # 2. Use the Sheety API to GET all the data in that sheet and print it out.

        response = requests.get(url=SHEETY_API_ENDPOINT, headers=headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data['prices']

        # 3. Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)

        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        headers = {
            'Authorization': AUTHORIZATION
        }

        for city in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(
                url=f"{SHEETY_API_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=headers
            )
            # pprint(response.text)

    # Set currency
    def update_currency(self):
        headers = {
            'Authorization': AUTHORIZATION
        }

        for city in self.destination_data:
            new_data = {
                'price': {
                    'currency': city['currency'],
                    'lowestPrice': city['lowestPrice']
                }
            }
            response = requests.put(
                url=f"{SHEETY_API_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=headers
            )
            # pprint(response.text)

    # Update price
    def update_price(self):
        headers = {
            'Authorization': AUTHORIZATION
        }

        for city in self.destination_data:
            new_data = {
                'price': {
                    'lowestPrice': city['lowestPrice'],
                    'currency': city['currency'],
                }
            }
            response = requests.put(
                url=f"{SHEETY_API_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=headers
            )
            # pprint(response.text)
