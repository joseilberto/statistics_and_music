from lxml.etree import tostring
from lxml.html import fromstring
from urllib.parse import urljoin, urlparse

import validators
import requests
import unidecode
import os
import sys

from .constants import RELEVANT_COLS, XPATHS
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
    def url_base(self):
        parser = urlparse(self.url)
        return parser.scheme + "://" + parser.netloc + "/"


    @property
    def out_path(self):
        out_path = self.kwargs.get("out_path", None)
        if not out_path:
            raise Exception("An output folder has not been specified")
        return self.kwargs["out_path"]


    @property
    def redownload(self):
        return self.kwargs.get("redownload", True)



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
            songs[i] = remove_punctuation(song, [".", "\n", ","], "\n",
                                        separator = ' ')
            songs_folder.append(artist_folder + songs[i] + self.bar)
            os.makedirs(artist_folder + songs[i] + self.bar, exist_ok = True)
        with open(artist_folder + "songs_summary.txt", "w") as file1:
            for song in songs:
                file1.write(song + "\n")
        tables = [fromstring(tostring(table)) for table in
                                                doc.xpath(XPATHS["table"])]
        for i, table in enumerate(tables):
            song_data = {}
            cols_idxs = {}
            lines = [fromstring(tostring(line)) for line in
                                            table.xpath(XPATHS["lines_table"])]
            file2 = open(songs_folder[i] + songs[i] + "_summary.txt", "w")
            table_data = []
            for idx, line in enumerate(lines):
                line_data = []
                if idx == 0:
                    cols = [col.replace(" ", "").lower()
                            for col in line.xpath(XPATHS["cols_table"]("h"))]
                    for idx_col, col in enumerate(cols):
                        if col in RELEVANT_COLS:
                            song_data[col] = []
                            cols_idxs[idx_col] = col
                            line_data.append(col)
                else:
                    first_col = [col.lower().replace(".", "_").replace(" ", "")
                            for col in line.xpath(XPATHS["cols_table"]("d[1]/a"))]
                    cols = first_col + [col.lower()
                            for col in line.xpath(XPATHS["cols_table"]("d"))]
                    for idx_col, col in enumerate(cols):
                        if idx_col in cols_idxs.keys():
                            song_data[cols_idxs[idx_col]].append(col)
                            line_data.append(col)
                    midi_file = line.xpath(XPATHS["link_midi"])
                    midi_url = urljoin(self.url_base, midi_file[0])
                    folder = songs_folder[i]
                    song_name = song_data["part"][-1]
                    if not os.path.isfile(folder + song_name) or self.redownload:
                        self.save_midi(midi_url, folder, song_name)
                file2.write(",".join(line_data))
                file2.write("\n")
                table_data.append(line_data)                


    def get_first_page(self, *args, **kwargs):
        response = requests.get(self.url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        links = doc.xpath(XPATHS["links_table"])
        for link in links:
            artist_url = urljoin(self.url_base, link)
            self.get_artist_midis(artist_url)


    def save_midi(self, url, folder, song, *args, **kwargs):
        response = requests.get(url, allow_redirects = True)
        if response.status_code <= 400:
            open(folder + song + ".mid", "wb").write(response.content)
