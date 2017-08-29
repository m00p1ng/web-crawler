import os
from urllib.parse import urlparse

from .content_filter import ContentFilter
from .robots_parser import RobotsParser
from .url_extractor import URLExtractor
from .url_filter import URLFilter
from ..utils import check_extension
from ..urls import url_to_path
from ..settings import SEED_HOSTNAME


class Analyzer:
    def __init__(self, url, content):
        self.url = url
        self.url_parse = urlparse(url)
        self.content = content

    def start(self):
        is_duplicated = self._content_analyzer()
        if is_duplicated:
            return [], is_duplicated
        else:
            return self._url_analyzer(), is_duplicated

    def _content_analyzer(self):
        cf = ContentFilter(self.url_parse, self.content)
        return cf.filter_duplicated()

    def _url_analyzer(self):
        ue = URLExtractor(self.url_parse, self.content, SEED_HOSTNAME)
        urls = ue.extract_link()

        if urls:
            urls = [url for url in urls if self._filter_extension(url)]

            uf = URLFilter(urls)
            urls = uf.filter_links()

        return urls

    def _filter_extension(self, url):
        filename = url_to_path(url).filename
        return check_extension(filename)
