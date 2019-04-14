from math import ceil

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from .parsers import parse_data


class PlotSigmaEntropy:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    @property
    def colors(self):
        return ["k", "b", "g", "y", "m", "c", "orange", "pink", "lime",
                    "slategray", "crimson", "gold", "mediumpurple", "indigo",
                    "palevioletred", "olive", "bisque", "lightcoral",
                    "rosybrown", "moccasin", "darkorange", "wheat", "khaki"]


    @parse_data
    def plot_property(self, pieces, artist, song, property = "sigma",
                                                            *args, **kwargs):
        base_folder = os.path.dirname(pieces[0]) + "/csv_files/sigma_entropy/"
        output_folder = '/'.join(os.path.dirname(pieces[0]).split("/")[:4])
        output_folder = output_folder + "/summary/"
        os.makedirs(output_folder, exist_ok = True)
        pattern = ("{}_{}_ENTROPY.pdf" if "entropy" in property
                                        else "{}_{}_SIGMA.pdf")
        output_fig = output_folder + pattern.format(artist, song)
        fig, ax = plt.subplots()
        xmax, ymax = 0, 0
        for idx, piece in enumerate(pieces):
            file_name = os.path.basename(piece).replace(".mid",
                                                        "_statistics.csv")
            piece_name = os.path.basename(piece).replace(".mid", "")
            file = base_folder + file_name
            data = pd.read_csv(file).dropna()
            if data.empty:
                continue
            xmax = data["k"].max() if data["k"].max() > xmax else xmax
            ymax = (1 + ceil(data[property].max())
                        if 1 + ceil(data[property].max()) > ymax
                        else ymax)
            idx_color = (idx if idx < len(self.colors)
                                else idx - len(self.colors))
            ax.scatter(data["k"], data[property], c = self.colors[idx_color],
                                    alpha = 0.5, label = piece_name)
        ks = np.arange(3, xmax + 1)
        if "sigma" in property:
            sigmas_geometric = np.sqrt(ks - 1)
            ax.plot(ks, sigmas_geometric, color = 'r', label = r"$\sqrt{k - 1}$")
            ax.set_ylabel(r"$\sigma(k)$")
        elif "entropy" in property:
            entropy_geometric = np.log(ks - 1)
            ax.plot(ks, entropy_geometric, color = 'r', label = r"$\ln{k - 1}$")
            ax.set_ylabel(r"$H_g(k)$")
        ax.legend(loc = "upper left", fontsize = 5)
        ax.set_xlabel(r"$k$")
        ax.set_title(song)
        ax.set_xscale("log")
        xmax_round = 10**(2) if xmax < 10**(2) else 10**(3)
        ax.set_ylim(-1, ymax)
        ax.set_xlim(1, xmax_round)
        fig.savefig(output_fig, format = "pdf", bbox_inches = "tight")
        plt.close()
