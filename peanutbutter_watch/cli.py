import io
import json
import time
import click
from datetime import datetime
from peanutbutter_watch import Scraper
from peanutbutter_watch import logger


@click.command()
@click.argument(
    "url",
    default="https://de.myprotein.com/nutrition/healthy-food-drinks/nut-butters.list",
)
@click.option('--match', '-m', required=True)
def main(url, match):
    """scrapes the Berlin Police website for stolen bikes"""

    scraper = Scraper(url)

    results = scraper.run()
    while not results:
        logger.info("peanutbutter not available, trying again in 30 seconds")
        time.sleep(30)
        results = scraper.run()
    
    for product in results:
        price = product["price"]
        product_name = product["product_name"]
        if product_name == match:
            print("🥜🧈 PEANUT BUTTER PARTY 🎉")
            print(f'name: {product_name}')
            print(f'price: {price}')
            break
