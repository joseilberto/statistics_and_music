from lxml.etree import tostring
from lxml.html import fromstring
from urllib.parse import urljoin, urlparse

import validators
import requests
import unidecode
import os
import sys

from .constants import RELEVANT_COLS, XPATHS
from .utils import join_to_path, remove_punctuation, remove_special_characters


class My_Crawler:
    def __init__(self, url, *args, **kwargs):
        self._url = url
        self.args = args
        self.kwargs = kwargs


    @property
    def redownload(self):
        return self.kwargs.get("redownload", True)


    @property
    def url(self):
        if not validators.url(self._url):
            raise Exception("Invalid url format.")
        return self._url


    @property
    def url_base(self):
        parser = urlparse(self.url)
        return parser.scheme + "://" + parser.netloc + "/"


    def get_artist_midis(self, url, *args, **kwargs):
        response = requests.get(url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        artist = unidecode.unidecode(doc.xpath(XPATHS["artist"])[0]).lower()
        self.midi_files[artist] = {}
        artist_folder = join_to_path(self.out_path, artist)
        os.makedirs(artist_folder, exist_ok = True)
        songs = doc.xpath(XPATHS["songs"])
        songs_dict = {
                "artist": artist,
                "artist_folder": artist_folder,
                "doc": doc,
                    }
        self.get_songs(songs, **songs_dict)


    def get_pieces(self, tables, *args, **kwargs):
        for i, table in enumerate(tables):
            song_data = {}
            cols_idxs = {}
            lines = [fromstring(tostring(line))
                     for line in table.xpath(XPATHS["lines_table"])]
            file2 = open(kwargs["songs_folder"][i] + kwargs["songs"][i] +
                                            "_summary.txt", "w")
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
                    first_col = [remove_special_characters(
                        col.replace(".", "_").replace(" ", "").replace("'", ""))
                        for col in line.xpath(XPATHS["cols_table"]("d[1]/a"))]
                    cols = first_col + [remove_special_characters(col)
                        for col in line.xpath(XPATHS["cols_table"]("d"))]
                    for idx_col, col in enumerate(cols):
                        if idx_col in cols_idxs.keys():
                            song_data[cols_idxs[idx_col]].append(col)
                            line_data.append(col)
                    midi_file = line.xpath(XPATHS["link_midi"])
                    midi_url = urljoin(self.url_base, midi_file[0])
                    folder = kwargs["songs_folder"][i]
                    song_name = song_data["part"][-1]
                    song_file = folder + song_name + ".mid"
                    self.midi_files[kwargs["artist"]][
                                        kwargs["songs"][i]].append(song_file)
                    if not os.path.isfile(song_file) or self.redownload:
                        self.save_midi(midi_url, song_file)
                file2.write(",".join(line_data))
                file2.write("\n")
                table_data.append(line_data)


    def get_songs(self, songs, *args, **kwargs):
        songs_folder = []
        for i, song in enumerate(songs):
            songs[i] = remove_punctuation(song, [".", "\n", ",", "'", ":"], "\n",
                                        separator = ' ')
            song_folder = join_to_path(kwargs["artist_folder"], songs[i])
            songs_folder.append(song_folder)
            os.makedirs(song_folder, exist_ok = True)
            self.midi_files[kwargs["artist"]][songs[i]] = []
        with open(kwargs["artist_folder"] + "songs_summary.txt", "w") as file1:
            for song in songs:
                file1.write(song + "\n")
        tables = [fromstring(tostring(table)) for table in
                                        kwargs["doc"].xpath(XPATHS["table"])]
        pieces_dict = kwargs.copy()
        pieces_dict.update({
            "songs_folder": songs_folder,
            "songs": songs,
        })
        self.get_pieces(tables, **pieces_dict)


    def get_first_page(self, *args, **kwargs):
        response = requests.get(self.url)
        if response.status_code >= 400:
            raise Exception("The url is not responding.")
        doc = fromstring(response.content)
        links = doc.xpath(XPATHS["links_table"])
        for link in links:
            artist_url = urljoin(self.url_base, link)
            self.get_artist_midis(artist_url)


    def save_midi(self, url, song_file, *args, **kwargs):
        response = requests.get(url, allow_redirects = True)
        if response.status_code <= 400:
            open(song_file, "wb").write(response.content)
