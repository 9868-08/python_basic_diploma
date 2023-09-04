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
    "propertyId": "9209612"
}  # дефолтые значения с сайта


response = requests.request("POST", "https://hotels4.p.rapidapi.com/properties/v2/detail", json=payload,
                            headers=headers)
response_json = response.json()

print(response_json)

f = open("response.json", "a")
f.write(str(response_json))
f.close()

