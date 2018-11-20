import requests
from urllib.parse import urljoin
import lxml.html.soupparser as html
from lxml.cssselect import CSSSelector
from .logs import get_logger


logger = get_logger(__name__)


class HTMLResponse(object):
    """wrapper around requests.HttpResponse"""

    def __init__(self, response):
        self.response = response
        self.dom = html.fromstring(response.text)

    def query(self, css_selector):
        """performs a CSS select
        """
        sel = CSSSelector(css_selector)
        return sel(self.dom) or []

    def first_occurrence_of(self, css_selector):
        """shortcut for calling ``.query()[0]`` automatically handling when it
        an empty result could cause IndexError
        """
        for result in self.query(css_selector):
            # return first result ;)
            return result


class Scraper(object):
    def __init__(self, entrypoint_url):
        self.entrypoint_url = entrypoint_url
        self.http = requests.Session()

    def request(self, url):
        logger.debug(f'requesting url "{url}"')
        full_url = self.make_full_url(url)
        response = self.http.get(full_url)
        return HTMLResponse(response)

    def make_full_url(self, url):
        return urljoin(self.entrypoint_url, url)

    def run(self):
        response = self.request(self.entrypoint_url)
        result = []
        while response:
            items = response.query(".html5-section.modul-teaser.teaser") or []
            result.extend(map(self.extract_data_from_thumbnail, items))
            next_url = self.extract_url_for_next_page(response)
            if next_url:
                logger.debug(f"found url for next page: {next_url}")
                response = self.request(next_url)
            else:
                break

        return result

    def extract_url_for_next_page(self, response):
        link = response.first_occurrence_of("ul li.next.pager-item a")
        if link is not None:
            return

        return link.attrib.get("href")

    def scrape_bike_page(self, url):
        extra_data = []
        result = {"url": self.make_full_url(url)}

        response = self.request(url)
        title = response.first_occurrence_of("h1.title")
        if title is not None:
            result["description"] = title.text

        image = response.first_occurrence_of(".article .body .block .main-image a")
        if image is not None:
            result["image"] = self.make_full_url(image.attrib.get("src"))

        keys = [
            "operation_number",
            "kind_of_bike",
            "manufacturer",
            "model",
            "color",
            "department",
        ]
        for li in response.query(".body .list-tablelist li"):
            if not keys:
                next_expected_key = None
            else:
                next_expected_key = keys.pop(0)

            cells = [(x.text or "").strip() for x in li.cssselect(".cell p")][0:2]

            if not cells:
                continue

            value = cells[-1]
            if next_expected_key and value:
                result[next_expected_key] = value
            else:
                extra_data.extend(cells)

        extra_data = list(filter(bool, extra_data))
        if extra_data:
            result["extra_data"] = extra_data

        return result

    def extract_data_from_thumbnail(self, div):
        # .cssselect() returns multiple items but we only care about
        # the first one
        anchors = div.cssselect(".image a")
        if not anchors:
            return {}

        link = anchors[0]
        url = link.attrib.get("href")
        return self.scrape_bike_page(url)
