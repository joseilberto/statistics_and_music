from os.path import join
from shutil import rmtree
from time import sleep
from tqdm import tqdm

import os
import sys
import pandas as pd

from .constants import NOTES_DICT
from .processors import Properties_Calculator


class MidiToCSV(Properties_Calculator):
    def __init__(self, *args, **kwargs):
        self.csv_files = []
        self.args = args
        self.kwargs = kwargs


    @property
    def matlab_base(self):
        return self.kwargs.get("matlab_base", join("~", "MATLAB", "R2018a"))


    @property
    def matlab(self):
        return join(self.matlab_base, "bin", "matlab")


    @property
    def miditoolbox_path(self):
        return join(self.matlab_base, "toolbox", "matlab", "miditoolbox")


    @property
    def matlab_command(self):
        first_string = "matlab" if 'win' not in sys.platform else self.matlab 
        base_command = ('cd transform && {0} -nodisplay - nosplash ' +
                        '-nodesktop -r "converter({1}, {1}, {2});exit;" ' +
                        '| tail -n +10').format
        return base_command(first_string, "{}", 
                            "'{}'".format(self.miditoolbox_path)).format


    @property
    def redo_csv(self):
        return self.kwargs.get("redo_csv", False)


    @property
    def redo_transformed(self):
        return self.kwargs.get("redo_transformed", False)


    def midi_to_notes(self, piece, *args, **kwargs):
        base_folder = join(os.path.dirname(piece), "csv_files")
        if self.redo_csv:
            rmtree(base_folder)
        os.makedirs(base_folder, exist_ok = True)
        output_file = os.path.basename(piece).replace(".mid", ".csv")
        output_file = join(base_folder, output_file)
        self.csv_files.append(output_file)
        if not os.path.isfile(output_file) or self.redo_csv:
            os.system(self.matlab_command("'{}'".format(piece),
                                        "'{}'".format(output_file)))
            sleep(1)
            

    def transform_data(self, files, *args, **kwargs):
        pbar = tqdm(total = len(files), desc = "Miditoolbox processing")
        for artist, song in files.items():
            for song, pieces in song.items():
                for piece in pieces:
                    self.midi_to_notes(piece)
            pbar.update(1)
        pbar.close()
        self.transform_raw_to_structured(self.csv_files)


    def transform_raw_to_structured(self, files, *args, **kwargs):
        def note_beat_index(row):
            return row["note"] + "_" + str(round(row["DeltaT_beats"], 3))

        transformed_csv_files = []
        for file in files:
            transformed_file = file.replace(".csv", "_transformed.csv")
            transformed_csv_files.append(transformed_file)
            if not os.path.isfile(transformed_file) or self.redo_transformed:
                transformed_data = pd.DataFrame()
                data = pd.read_csv(file)
                data["note"] = data["note_number"].map(NOTES_DICT)
                transformed_data["note"] = data.apply(note_beat_index, axis = 1)
                transformed_data["channel"] = data["channel"]
                transformed_data["t_seconds"] = data["t_seconds"]
                transformed_data["DeltaT_seconds"] = data["DeltaT_seconds"]
                transformed_data.sort_values(by = ["t_seconds", "channel"],
                                                    inplace = True)
                transformed_data.to_csv(transformed_file, index = False)
        self.create_sigma_entropy_files(transformed_csv_files)
        self.create_time_series_files(transformed_csv_files)
