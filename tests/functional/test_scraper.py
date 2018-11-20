import vcr
from pathlib import Path
from sure import scenario
from berlin_bike_watch import Scraper

my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir=str(Path(__file__).parent.joinpath("cassettes")),
    record_mode='once',
    match_on=["uri", "method", "path", "query"],
)


@my_vcr.use_cassette
def test_scrape_male_bikes():
    "Scraper#scrape(url) should scrape pages with male bikes"

    engine = Scraper("https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/")
    results = engine.run()
    results.should.have.length_of(255)


@my_vcr.use_cassette
def test_scrape_female_bikes():
    "Scraper#scrape(url) should scrape pages with female bikes"

    engine = Scraper("https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/damenfahrraeder/")
    results = engine.run()
    results.should.have.length_of(148)



@my_vcr.use_cassette
def test_scrape_children_bikes():
    "Scraper#scrape(url) should scrape pages with children bikes"

    engine = Scraper("https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/kinderfahrraeder/")
    results = engine.run()
    results.should.have.length_of(18)


@my_vcr.use_cassette
def test_scrape_miscelaneous_bikes():
    "Scraper#scrape(url) should scrape pages with miscelaneous bikes"

    engine = Scraper("https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/sonstige-fahrraeder/")
    results = engine.run()
    results.should.have.length_of(19)


@my_vcr.use_cassette
def test_scrape_mutilated_bikes():
    "Scraper#scrape(url) should scrape pages with mutilated bikes"

    engine = Scraper("https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/fahrradteile/")
    results = engine.run()
    results.should.have.length_of(23)
