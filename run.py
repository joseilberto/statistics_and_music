import argparse
import os

from extract.SETTINGS import MIDI_URL
from crawler import get_and_store_midis


def set_args():
    """
    Set all arguments and return them parsed.
    """
    args_dic = {
        '-p': ['--path', str, 'Define the folder to save files.'],
    }
    parser = argparse.ArgumentParser(description = 'Process video files '
                                    'extracting the centers of each bead.')
    for key, value in args_dic.items():
        parser.add_argument(key, value[0], type = value[1], help = value[2])
    return parser.parse_args()


def process_args(arguments = set_args()):
    """
    Process the arguments got from argparse. Also sets the standard values if
    not given.
    """
    output_path = arguments.path
    os.makedirs(output_path, exist_ok = True)
    return output_path


if __name__ == "__main__":
    output_path = process_args()
    get_and_store_midis(MIDI_URL, output_path)