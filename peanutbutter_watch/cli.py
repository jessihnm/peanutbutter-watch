import io
import json
import click
from datetime import datetime
from peanutbutter_watch import Scraper
from peanutbutter_watch import logger


@click.command()
@click.argument(
    "url",
    default="https://de.myprotein.com/nutrition/healthy-food-drinks/nut-butters.list",
)
def main(url):
    """scrapes the Berlin Police website for stolen bikes"""

    scraper = Scraper(url)

    data = scraper.run()
