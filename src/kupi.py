'''
TODO: WRITE OWN PARSER!!!
The pykupi parser im using does not provide access to drink amount
eg. 6 bottles = higher price -> I am filtering those offers out;
This file will (eventually, hopefully) get a big rewrite
'''

import asyncio
from pykupi import KupiParser
from models import session, Drink, Store, store_drink_association


async def update():
    parser = KupiParser()
    drinks = session.query(Drink).all()
    stores = session.query(Store).all()
    # simplify access to available stores to build relation for drinks
    stores_table = {store.name: store for store in session.query(Store).all()}

    try:
        for drink in drinks:
            raw = await parser.get_prices(drink.name)

            # filter out offers from obscure stores nobody knows
            # unreadable line but works
            filtered_offers = [offer for offer in raw.offers if offer.offered_by.lower() in stores_table]

            if filtered_offers:
                cheapest = filtered_offers[0].price
                if cheapest < drink.normal_cost:
                    drink.discount = True
                    drink.discount_cost = cheapest

                    # store association - all this for a small icon of a store where the discount is
                    display_store_name = filtered_offers[0].offered_by.lower()
                    drink.store = stores_table[display_store_name]
            
            session.commit()

    finally:
        await parser.session.close()


if __name__ == "__main__":
    asyncio.run(update())