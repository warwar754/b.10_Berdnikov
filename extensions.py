import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class converter:
    @staticmethod
    def converter(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(
                "Нельзя переводить волюту саму в себя")
        try:
            quote = keys[quote]
        except KeyError:
            raise ConvertionException(
                f"Бот не знает валюту {quote}. Список доступных валют можно посмотреть командой /valute")
        try:
            base = keys[base]
        except KeyError:
            raise ConvertionException(
                f"Бот не знает валюту {base}. Список доступных валют можно посмотреть командой /valute")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(
                f"Значение {amount} не является числом")

    def get_price(quote: str, base: str, amount: str):
        quote_ticker = keys[quote]
        base_ticker = keys[base]
        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")

        result = (float(json.loads(r.content)[keys[base]]) * float(amount))

        return result
