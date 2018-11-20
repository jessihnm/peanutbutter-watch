import vcr
from pathlib import Path
from sure import scenario
from berlin_bike_watch import Scraper

import vcr

def jurassic_matcher(r1, r2):
    assumptions = [
        r1.uri == r2.uri,
        r1.query == r2.query,
    ]
    return all(assumptions)

my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir=str(Path(__file__).parent.joinpath("cassettes")),
    # record_mode="all",
    # record_mode="new_episodes",
)
my_vcr.register_matcher('jurassic', jurassic_matcher)
my_vcr.match_on = ['jurassic']


@my_vcr.use_cassette
def test_scrape_male_bikes():
    "Scraper#scrape(url) should scrape pages with male bikes"

    engine = Scraper(
        "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/"
    )
    results = engine.run()
    results.should.have.length_of(255)

    results[0].should.equal(
        {
            "color": "metallicgrau",
            "department": "Direktion 4 Abschnitt 41",
            "description": "Metallicgraues Herrenfahrrad",
            "image": "https://www.berlin.de/polizei/_assets/service/anlagen-fahrraddatenbank/759671.jpg",
            "kind_of_bike": "Herrenrad/ Rennrad",
            "manufacturer": "Cube",
            "model": "Streamer",
            "operation_number": "181116-0530-318740",
            "url": "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/artikel.759671.php",
        }
    )


@my_vcr.use_cassette
def test_scrape_female_bikes():
    "Scraper#scrape(url) should scrape pages with female bikes"

    engine = Scraper(
        "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/damenfahrraeder/"
    )
    results = engine.run()
    results.should.have.length_of(148)


@my_vcr.use_cassette
def test_scrape_children_bikes():
    "Scraper#scrape(url) should scrape pages with children bikes"

    engine = Scraper(
        "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/kinderfahrraeder/"
    )
    results = engine.run()
    results.should.have.length_of(18)


@my_vcr.use_cassette
def test_scrape_miscelaneous_bikes():
    "Scraper#scrape(url) should scrape pages with miscelaneous bikes"

    engine = Scraper(
        "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/sonstige-fahrraeder/"
    )
    results = engine.run()
    results.should.have.length_of(19)


@my_vcr.use_cassette
def test_scrape_mutilated_bikes():
    "Scraper#scrape(url) should scrape pages with mutilated bikes"

    engine = Scraper(
        "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/fahrradteile/"
    )
    results = engine.run()
    results.should.have.length_of(23)
