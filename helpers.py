from pip._vendor import requests
from datetime import datetime, timedelta
import pytz

def sort_by_date(items):
    return sorted(items, key = lambda item: item["date"])

def convert_to_pln(currency: str, amount: float, created_at: datetime):
    response = None
    bid = None

    if (currency != "PLN"):
        response = requests.get("http://api.nbp.pl/api/exchangerates/rates/c/" + currency + "/" + created_at.strftime("%Y-%m-%d"))
        """if date for NBP is not working day, response is 404, that is why day has to be substracted and it has to be checked until response is 200"""
        while(response.status_code != 200):
            created_at = created_at - timedelta(days=1)
            response = requests.get("http://api.nbp.pl/api/exchangerates/rates/c/" + currency + "/" + created_at.strftime("%Y-%m-%d"))
        bid = response.json()['rates'][0]['bid']
        converted = int(amount * bid)
    else: 
        return amount
    return converted

def make_card_info(name: str, surname: str, number: int):
    hidden_number = None
    list_number = list(str(number))
    for i in range(0, len(list_number)):
        if(i > 3 and i < 12):
            list_number[i] = "*"
    hidden_number = "".join(list_number)
    return name + " " + surname + " " + hidden_number

def convert_to_utc(date: str):
    return date.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
