import numpy as np
import os
import pandas as pd


class Properties_Calculator:
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
            rel_data = self.calculate_sigma_and_entropy(file)
            
