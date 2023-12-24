import os
import shutil


def clear_directory(path_to_save_files, file_name_prefix=None):
    if file_name_prefix:
        for filename in os.listdir(path_to_save_files):
            if filename.startswith(file_name_prefix):
                file_path = os.path.join(path_to_save_files, filename)
                os.remove(file_path)
    else:
        shutil.rmtree(path_to_save_files)
        os.makedirs(path_to_save_files, exist_ok=True)
