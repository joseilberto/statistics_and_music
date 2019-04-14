def parse_data(method):
    def wrapper(self, files, property, *args, **kwargs):
        for artist, song in files.items():
            for song, pieces in song.items():
                method(self, pieces, artist, song, property, *args, **kwargs)
    return wrapper
