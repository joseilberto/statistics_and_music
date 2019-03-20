from lxml.etree import tostring
from lxml.html import fromstring
from urllib.parse import urljoin, urlparse

import validators
import requests
import unidecode
import os
import sys

from .constants import XPATHS
from .utils import remove_punctuation


class My_Crawler:
    def __init__(self, url, *args, **kwargs):
        self._url = url
        self.args = args
        self.kwargs = kwargs


    @property
    def bar(self):
        return '/' if 'win' not in sys.platform else '\\'


    @property
    def url(self):
        if not validators.url(self._url):
            raise Exception("Invalid url format.")
        return self._url


    @property
    def out_path(self):
        out_path = self.kwargs.get("out_path", None)
        if not out_path:
            raise Exception("An output folder has not been specified")
        return self.kwargs["out_path"]


    def get_artist_midis(self, url, *args, **kwargs):
        response = requests.get(url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        artist = unidecode.unidecode(doc.xpath(XPATHS["artist"])[0]).lower()
        artist_folder = self.out_path + artist + self.bar
        os.makedirs(artist_folder, exist_ok = True)
        songs = doc.xpath(XPATHS["songs"])
        songs_folder = []
        for i, song in enumerate(songs):
            songs[i] = remove_punctuation(song, ["\n", ","], "\n",
                                        separator = ' ')
            songs_folder.append(artist_folder + songs[i] + self.bar)
        tables = [fromstring(tostring(table)) for table in
                                                doc.xpath(XPATHS["table"])]
        for idx, table in enumerate(tables):
            lines = [fromstring(tostring(line)) for line in
                                            table.xpath(XPATHS["lines_table"])]
            for line in lines:
                #TODO Finish the line extraction


    def get_first_page(self, *args, **kwargs):
        parser = urlparse(self.url)
        url_base = parser.scheme + "://" + parser.netloc + "/"
        response = requests.get(self.url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        links = doc.xpath(XPATHS["links_table"])
        for link in links:
            artist_url = urljoin(url_base, link)
            self.get_artist_midis(artist_url)
