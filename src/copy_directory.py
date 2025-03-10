"""This module contains the function for copying the static content in to the public directory"""

import os
import shutil


def copy_directory_recursive(src: str, dest: str):
    """
    Recursively copies all contents from src to dest.
    Deletes all existing content in dest before copying.

    Args:
        src (str): Source directory path.
        dest (str): Destination directory path.
    """
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return

    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted all contents of '{dest}'")

    os.makedirs(dest, exist_ok=True)

    for root, dirs, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, relative_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)
            print(f"Copied '{src_file}' to '{dest_file}'")

        for directory in dirs:
            os.makedirs(os.path.join(dest_dir, directory), exist_ok=True)
            print(f"Created directory '{os.path.join(dest_dir, directory)}'")
