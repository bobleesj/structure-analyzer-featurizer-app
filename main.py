import os
import time

from cifkit import Cif
from cifkit.utils.folder import get_file_paths
from pandas import DataFrame as df
from SAF.features.generator import (
    compute_binary_features,
    compute_quaternary_features,
    compute_ternary_features,
)

from core import folder, prompt


# Choose the folder
def main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(dir_names_with_cif, ".cif")

    num_selected_dirs = len(selected_dirs)
    for idx, (_, dir_path) in enumerate(selected_dirs.items(), start=1):
        prompt.prompt_folder_progress(idx, dir_path, num_selected_dirs)
        process_cifs(dir_path)


def process_cifs(dir_path):
    file_paths = get_file_paths(dir_path)
    binary_data = []
    ternary_data = []
    quaternary_data = []
    uni_data = []
    for i, file_path in enumerate(file_paths, start=1):
        file_start_time = time.perf_counter()
        try:
            cif = Cif(file_path)
            prompt.prompt_progress_current(
                i, file_path, cif.supercell_atom_count, len(file_paths)
            )
        except Exception as e:
            print(f"Could not read the .cif file of {file_path}. Reason:", e)
            continue
        try:
            if len(cif.unique_elements) == 2:
                features, uni_features = compute_binary_features(file_path)
                binary_data.append(features)
                uni_data.append(uni_features)
            if len(cif.unique_elements) == 3:
                features, uni_features = compute_ternary_features(file_path)
                ternary_data.append(features)
                uni_data.append(uni_data)
            if len(cif.unique_elements) == 4:
                features, uni_features = compute_quaternary_features(file_path)
                ternary_data.append(features)
                uni_data.append(uni_data)
        except Exception as e:
            print(f"Error found for {file_path}. Reason: {e}")
            continue
        elapsed_time = time.perf_counter() - file_start_time
        prompt.prompt_progress_finished(
            cif.file_name, cif.supercell_atom_count, elapsed_time
        )
    # Save
    csv_folder_path = os.path.join(dir_path, "csv")
    binary_csv_path = os.path.join(csv_folder_path, "binary_features.csv")
    ternary_csv_path = os.path.join(csv_folder_path, "ternary_features.csv")
    quaternary_csv_path = os.path.join(csv_folder_path, "quaternary_features.csv")
    universal_csv_path = os.path.join(csv_folder_path, "universal_features.csv")
    os.makedirs(csv_folder_path, exist_ok=True)
    if binary_data:
        df(binary_data).round(3).to_csv(binary_csv_path)
        prompt.prompt_file_saved(binary_csv_path)
    if ternary_data:
        df(ternary_data).round(3).to_csv(ternary_csv_path, index=False)
        prompt.prompt_file_saved(ternary_csv_path)
    if quaternary_data:
        df(quaternary_data).round(3).to_csv(ternary_csv_path, index=False)
        prompt.prompt_file_saved(quaternary_csv_path)
    if binary_data or ternary_data or quaternary_data:
        df(uni_data).round(3).to_csv(universal_csv_path, index=False)
        prompt.prompt_file_saved(universal_csv_path)


if __name__ == "__main__":
    main()
