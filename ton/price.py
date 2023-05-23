from pycoingecko import CoinGeckoAPI


def ton_price():
    cg = CoinGeckoAPI()
    response = cg.get_price(ids='the-open-network', vs_currencies='usd')
    price = response['the-open-network']['usd']
    return f'Toncoin: ${price}'

