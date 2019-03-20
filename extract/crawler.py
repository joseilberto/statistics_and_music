from .processors import My_Crawler


class Crawler(My_Crawler):
    def __init__(self, url, *args, **kwargs):
        super(Crawler, self).__init__(url, *args, **kwargs)


    @property
    def download(self):
        kwargs = self.kwargs.get("download", True)
        return kwargs


    def get_and_store_midis(self, *args, **kwargs):
        if self.download:
            self.get_first_page()
