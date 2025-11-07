import json
import os
from typing import Any

def read_json_file(filepath: str) -> Any:
    json_data = None
    with open(filepath) as file:
        json_data = json.load(file)
    return json_data

def write_json_file(data, filename):
    """
    This file contain the method ``write_json_file``. It opens the a file with the given name and writes all the given data
    to the file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent='\t')
