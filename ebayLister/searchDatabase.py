import requests
import json

def searchDatabase(searchTerm):
    url = (f'http://127.0.0.1:8000/api/dvd/?search={searchTerm}')
    response = requests.get(url)

    data = response.text
    return data