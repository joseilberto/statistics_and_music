import os


class MidiToCSV:
    def __init__(self, *args, **kwargs):
        self.csv_files = []
        self.args = args
        self.kwargs = kwargs


    @property
    def redo_csv(self):
        return self.kwargs.get("redo_csv", False)


    @property
    def matlab(self):
        return self.kwargs.get("matlab_route", "~/MATLAB/R2018a/bin/matlab")


    @property
    def miditoolbox_path(self):
        return self.kwargs.get("miditoolbox_path",
                                "~/MATLAB/R2018a/toolbox/matlab/miditoolbox")


    @property
    def matlab_command(self):
        base_command = ('cd transform && {0} -nodisplay - nosplash -nodesktop -r ' +
                        '"converter({1}, {1}, {2});exit;" | tail -n +10')
        return base_command.format(self.matlab, "{}",
                            "'{}'".format(self.miditoolbox_path)).format


    def midi_to_notes(self, piece, *args, **kwargs):
        base_folder = os.path.dirname(piece) + "/csv_files/"
        os.makedirs(base_folder, exist_ok = True)
        output_file = os.path.basename(piece).replace(".mid", ".csv")
        output_file = base_folder + output_file
        self.csv_files.append(output_file)
        if not os.path.isfile(output_file) or self.redo_csv:
            os.system(self.matlab_command("'{}'".format(piece),
                                        "'{}'".format(output_file)))


    def transform_data(self, files, *args, **kwargs):
        for artist, song in files.items():
            for song, pieces in song.items():
                for piece in pieces:
                    notes = self.midi_to_notes(piece)
