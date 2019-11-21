from .processors import PlotBarCode, PlotSigmaEntropy


class LoaderToPlot(PlotBarCode, PlotSigmaEntropy):
    def __init__(self, *args, **kwargs):        
        self.args = args
        self.kwargs = kwargs
