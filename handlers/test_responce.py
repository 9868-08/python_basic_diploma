import requests

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "f11fe670bamshdaffc29f3f33e2bp19bde9jsn5f0726b4228a",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "6054439"},
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2023
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2023
    },
    "rooms": [
        {
            "adults": 2,
            "children": [{"age": 5}, {"age": 7}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
        "max": 150,
        "min": 100
    }}
}

response = requests.request("POST", "https://hotels4.p.rapidapi.com/properties/v2/list", json=payload,
                            headers=headers)
response_json = response.json()

print(response_json)

f = open("response.json", "a")
f.write(str(response_json))
f.close()

