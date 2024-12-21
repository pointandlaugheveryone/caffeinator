'''
TODO: WRITE OWN PARSER!!!
The pykupi parser im using does not provide access to drink amount
eg. 6 bottles -> I am filtering those offers out;
This file will eventually get a big rewrite
'''

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
        filtered_offers = [offer for offer in raw.offers if offer.offered_by.lower() in stores]
        
        if filtered_offers:
            cheapest = filtered_offers[0]
            if cheapest < drink.normal_cost:
                drink.discount = True
                drink.discount_cost = cheapest

    await parser.session.close()

asyncio.run(update())