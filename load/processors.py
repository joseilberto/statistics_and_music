from .parsers import parse_data


class PlotSigmaEntropy:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    @parse_data
    def plot_sigma(self, pieces, song, *args, **kwargs):
        pass
