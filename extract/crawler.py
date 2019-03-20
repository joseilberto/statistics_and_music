from lxml.html import fromstring
from urllib.parse import urljoin, urlparse

import requests
import unidecode

from .constants import XPATHS
from .utils import remove_punctuation


def get_artist_midi(url, out_path, *args, **kwargs):
    response = requests.get(url)
    if response.status_code >= 400:
        raise Exception("The url is not responding.")
    doc = fromstring(response.content)
    artist = unidecode.unidecode(doc.xpath(XPATHS["artist"])[0])
    songs = doc.xpath(XPATHS["songs"])
    for song in songs:
        song = remove_punctuation(song)
    import ipdb; ipdb.set_trace()


def get_and_store_midis(url, out_path, download = True, *args, **kwargs):
    if download:
        parser = urlparse(url)
        url_base = parser.scheme + "://" + parser.netloc + "/"
        response = requests.get(url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        links = doc.xpath(XPATHS["table"])
        for link in links:
            artist_url = urljoin(url_base, link)
            get_artist_midis(artist_url, out_path, *args, **kwargs)
            
