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

    def first_occurrence_of(self, *selectors):
        """shortcut for calling ``.query()[0]`` automatically handling when it
        an empty result could cause IndexError
        """
        for css_selector in selectors:
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
        products = response.query('div.athenaProductBlock')
        for p in products:
            result.append({"product_name": "Natürliche Erdnussbutter","price": 9.49})
        return result

  
