import io
import json
import click
from datetime import datetime
from peanutbutter_watch import Scraper
from peanutbutter_watch import logger


@click.command()
@click.argument(
    "url",
    default="https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/",
)
@click.option(
    "-o",
    "--output-file",
    default="berlin-bikes-found-{}.json".format(
        datetime.now().strftime("%Y%m%d-%H%M%S")
    ),
)
def main(url, output_file):
    """scrapes the Berlin Police website for stolen bikes"""

    scraper = Scraper(url)

    data = scraper.run()

    with io.open(output_file, "w") as fd:
        fd.write(json.dumps(data, indent=2))

    logger.info(f"wrote scraped data to {output_file}")


if __name__ == "__main__":
    hello()
