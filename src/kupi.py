import asyncio
from pykupi import KupiParser
from models import session, Drink, Store, store_drink_association


async def update():
    parser = KupiParser()
    drinks = session.query(Drink).all()
    stores = {store.name for store in session.query(Store).all()}

    for drink in drinks:
        raw = await parser.get_prices(drink.Name)

        # filter out offers from obscure stores nobody knows
        filtered_offers = [offer for offer in raw.offers if offer.offered_by in stores]

        if filtered_offers:
            cheapest = filtered_offers[0]
            drink.discount_cost = cheapest

    await parser.session.close()
'''
test = await parser.get_prices("coca-cola-zero")

    print(test.high_price, test.low_price)
    for offer in test.offers:
        print(offer.offered_by, offer.price)
'''
    

asyncio.run(update())