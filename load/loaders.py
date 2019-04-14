class LoaderToPlot:
    def __init__(self, Plot_Class, *args, **kwargs):
        self.plotter = Plot_Class(*args, **kwargs)
