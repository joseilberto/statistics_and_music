from os.path import join

import numpy as np
import os
import pandas as pd


class Properties_Calculator:
    @property
    def redo_sigma_entropy(self):
        return self.kwargs.get("redo_sigma_entropy", False)


    @property
    def redo_time_series(self):
        return self.kwargs.get("redo_time_series", False)


    def calculate_sigma_and_entropy(self, file, skip_small_freq = True, *args, 
                                    **kwargs):
        def calculate_entropy(probabilities):
            entropy = 0
            for probability in probabilities:
                entropy -= probability*np.log(probability)
            return entropy

        data = pd.read_csv(file)
        columns = ["note", "k", "sigma", "entropy"]
        grouped = data.groupby("note")
        processed = []
        for note, cur_data in grouped:
            if len(cur_data) < 3 and skip_small_freq:
                continue
            elif len(cur_data) == 1:
                sigma = -1
                entropy = -1
            elif len(cur_data) == 2:
                sigma = 0
                entropy = 0
            elif len(cur_data) >= 3:
                differences = cur_data["t_seconds"].diff().dropna()
                sigma = differences.std() / differences.mean()
                grouped_differences = (differences.groupby(differences).count() /
                                                                len(differences))
                entropy = calculate_entropy(grouped_differences)
            processed.append([note, len(cur_data), sigma, entropy])
        return pd.DataFrame.from_records(processed, columns = columns)


    def create_sigma_entropy_files(self, files, *args, **kwargs):
        for file in files:
            base_folder = join(os.path.dirname(file), "sigma_entropy")
            file_base = os.path.basename(file).replace("_transformed",
                                                                "{}")
            os.makedirs(base_folder, exist_ok = True)
            output_base = join(base_folder, file_base).format
            output_file = output_base("_statistics")
            if not os.path.isfile(output_file) or self.redo_sigma_entropy:
                data = self.calculate_sigma_and_entropy(file)
                if len(data) == 0:
                    continue
                self.save_sigma_entropy_data(data, output_file)
                self.save_top10(data, output_base("_top10_frequency"), "k")
                self.save_top10(data, output_base("_top10_entropy"), "entropy")
                self.save_top10(data, output_base("_top10_sigma"), "sigma")

    
    def create_time_series_files(self, files, *args, **kwargs):
        for file in files:
            base_folder = join(os.path.dirname(file), "time_series")
            file_base = os.path.basename(file).replace("_transformed", "{}")
            
            os.makedirs(base_folder, exist_ok = True)
            output_base = join(base_folder, file_base).format
            output_file = output_base("_time_series")
            if not os.path.isfile(output_file) or self.redo_time_series:
                full_data = pd.read_csv(file)
                columns = ["t_seconds", "k", "sigma", "entropy"]                
                sigma_entropy_data = self.calculate_sigma_and_entropy(file, 
                                                        skip_small_freq = False)
                full_data = pd.merge(full_data, sigma_entropy_data, on = "note")
                rel_data = full_data[columns]
                self.save_time_series_data(rel_data, output_file)                


    def save_sigma_entropy_data(self, data, output_file, *args, **kwargs):
        data.sort_values(by = ["sigma"], ascending = False, inplace = True)
        data.to_csv(output_file, index = False)
    

    def save_time_series_data(self, data, output_file, *args, **kwargs):
        data.to_csv(output_file, index = False)
        


    def save_top10(self, data, output_file, column = "sigma", top = 10, *args,
                                                                    **kwargs):
        data.sort_values(by = [column], ascending = False, inplace = True)
        data.head(top).to_csv(output_file, index = False)
