import numpy as np
import os
import pandas as pd


class Properties_Calculator:
    @property
    def redo_sigma_entropy(self):
        return self.kwargs.get("redo_sigma_entropy", False)


    def calculate_sigma_and_entropy(self, file, *args, **kwargs):
        def calculate_entropy(probabilities):
            entropy = 0
            for probability in probabilities:
                entropy -= probability*np.log(probability)
            return entropy

        data = pd.read_csv(file)
        min_time_seconds = data["DeltaT_seconds"].min()
        columns = ["note", "k", "sigma", "entropy"]
        data["t_seconds"] = (data["t_seconds"] / min_time_seconds).round()
        grouped = data.groupby("note")
        processed = []
        for note, cur_data in grouped:
            if len(cur_data) < 3:
                continue
            differences = cur_data["t_seconds"].diff().dropna()
            sigma = differences.std() / differences.mean()
            grouped_differences = (differences.groupby(differences).count() /
                                                            len(differences))
            entropy = calculate_entropy(grouped_differences)
            processed.append([note, len(cur_data), sigma, entropy])
        return pd.DataFrame.from_records(processed, columns = columns)


    def create_sigma_entropy_files(self, files, *args, **kwargs):
        for file in files:
            base_folder = os.path.dirname(file) + "/sigma_entropy/"
            file_base = os.path.basename(file).replace("_transformed",
                                                                "{}")
            os.makedirs(base_folder, exist_ok = True)
            output_base = (base_folder + file_base).format
            output_file = output_base("_statistics")
            if not os.path.isfile(output_file) or self.redo_sigma_entropy:
                data = self.calculate_sigma_and_entropy(file)
                self.save_sigma_entropy_data(data, output_file)
                self.save_top10(data, output_base("_top10_frequency"), "k")
                self.save_top10(data, output_base("_top10_entropy"), "entropy")
                self.save_top10(data, output_base("_top10_sigma"), "sigma")


    def save_sigma_entropy_data(self, data, output_file, *args, **kwargs):
        data.sort_values(by = ["sigma"], ascending = False, inplace = True)
        data.to_csv(output_file, index = False)


    def save_top10(self, data, output_file, column = "sigma", top = 10, *args,
                                                                    **kwargs):
        data.sort_values(by = [column], ascending = False, inplace = True)
        data.head(top).to_csv(output_file, index = False)
