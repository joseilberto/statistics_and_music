def parse_data(method):
    def wrapper(self, files, *args, **kwargs):
        for artist, song in files.items():
            for song, pieces in song.items():                
                method(self, pieces, song, *args, **kwargs)
    return wrapper
