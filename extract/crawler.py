import os

from .processors import My_Crawler
from .utils import join_to_path


class Crawler(My_Crawler):
    def __init__(self, url, *args, **kwargs):
        self.midi_files = {}
        super(Crawler, self).__init__(url, *args, **kwargs)


    @property
    def download(self):
        return self.kwargs.get("download", True)


    @property
    def out_path(self):
        out_path = self.kwargs.get("out_path", None)
        if not out_path:
            raise Exception("An output folder has not been specified")
        return self.kwargs["out_path"]


    def find_midi_files(self):
        artists = [artist for artist in os.listdir(self.out_path)
                        if os.path.isdir(join_to_path(self.out_path, artist))]
        if not artists:
            self.get_first_page()

        for artist in artists:
            self.midi_files[artist] = {}
            artist_folder = join_to_path(self.out_path, artist)
            songs = [song for song in os.listdir(artist_folder)
                        if os.path.isdir(join_to_path(artist_folder, song))]
            for song in songs:
                song_folder = join_to_path(artist_folder, song)
                pieces = [song_folder + piece
                          for piece in os.listdir(song_folder)
                          if os.path.isfile(song_folder + piece) and
                                                    piece.endswith(".mid")]
                self.midi_files[artist][song] = pieces


    def get_and_store_midis(self, *args, **kwargs):
        if self.download:
            self.get_first_page()
        else:
            self.find_midi_files()
