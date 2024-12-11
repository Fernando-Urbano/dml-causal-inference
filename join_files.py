import numpy as np
import pandas as pd
import os
import glob

def get_script_files(directory=None, extension="puml"):
    if directory is None:
        directory = "."
    if isinstance(extension, str):
        extension = [extension]
    paths = []
    for ext in extension:
        paths += glob.glob(os.path.join(directory, f"*.{ext}"))
    return paths

def load_script_files(script_files):
    script_dict = {}
    for file in script_files:
        with open(file, 'r') as f:
            script_dict[file] = f.readlines()
    return script_dict

def list_to_text(script_dict, initial_text=""):
    divider = "\n\n" + "=" * 80 + "\n\n"
    script_text = initial_text
    if initial_text != "":
        script_text += divider
    for file_name, script in script_dict.items():
        script_text += "FILE NAME: " + file_name + "\n\n"
        for line in script:
            script_text += line
        script_text += divider
    return script_text

def text_to_file(text, filename):
    with open(filename + ".txt", 'w') as f:
        f.write(text)


def scripts_to_file(directory, extension, initial_text, filename, filter_files=None, ignore_files=None):
    script_files = get_script_files(directory, extension)
    if filter_files is not None:
        filter_files = [directory + "/" + file for file in filter_files]
        script_files = [file for file in script_files if file in filter_files]
    if ignore_files is not None:
        ignore_files = [directory + "/" + file for file in ignore_files]
        script_files = [file for file in script_files if file not in ignore_files]
    script_list = load_script_files(script_files)
    script_text = list_to_text(script_list, initial_text)
    text_to_file(script_text, filename)

if __name__ == "__main__":

    if os.path.exists("scripts"):
        os.system("rm -r scripts")
    os.mkdir("scripts")
    scripts_to_file("tests", "py", "Test files:", "scripts/tests", ignore_files=["__init__.py"])
    scripts_to_file("scenarios", "py", "Causal Scenario file:", "scripts/scenarios", ignore_files=["__init__.py"])
    scripts_to_file("database/init", ["py", "sql"], "Database initialization:", "scripts/database", ignore_files=["__init__.py"])
    scripts_to_file("simulations", ["py"], "Simulations running:", "scripts/simulations", ignore_files=["__init__.py"])
    scripts_to_file("scripts", "txt", "All files", "scripts/all")