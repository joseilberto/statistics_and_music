from lxml.etree import tostring
from lxml.html import fromstring
from urllib.parse import urljoin, urlparse

import requests
import unidecode
import os

from .constants import XPATHS
from .utils import remove_punctuation


def get_artist_midis(url, out_path, *args, **kwargs):
    response = requests.get(url)
    if response.status_code >= 400:
        raise Exception("The url is not responding.")
    doc = fromstring(response.content)
    artist = unidecode.unidecode(doc.xpath(XPATHS["artist"])[0]).lower()
    artist_folder = out_path + artist + "/"
    os.makedirs(artist_folder, exist_ok = True)
    songs = doc.xpath(XPATHS["songs"])
    songs_folder = []
    for i, song in enumerate(songs):
        songs[i] = remove_punctuation(song, ["\n", ","], "\n", separator = ' ')
        songs_folder.append(artist_folder + songs[i] + "/")
    tables = [fromstring(tostring(table)) for table in
                                                    doc.xpath(XPATHS["table"])]
    for idx, table in enumerate(tables):
        lines = [fromstring(tostring(line)) for line in
                                            table.xpath(XPATHS["lines_table"])]
        for line in lines:
            # TODO Finish it


def get_and_store_midis(url, out_path, download = True, *args, **kwargs):
    if download:
        parser = urlparse(url)
        url_base = parser.scheme + "://" + parser.netloc + "/"
        response = requests.get(url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        links = doc.xpath(XPATHS["links_table"])
        for link in links:
            artist_url = urljoin(url_base, link)
            get_artist_midis(artist_url, out_path, *args, **kwargs)
