
import requests

def postData(searchTerm, title, cexImageUrl, booktopiaImageUrl, cexSell, cexBuy, cexTrade):

    payload = {
        'barcode': int(searchTerm),
        'title': title,
        'cexPhotoUrl': cexImageUrl,
        'booktopiaPhotoUrl': booktopiaImageUrl,
        'cexSell': cexSell,
        'cexBuy': cexBuy,
        'cexTrade': cexTrade
    }

    requests.post('http://127.0.0.1:8000/api/dvd/', data=payload)