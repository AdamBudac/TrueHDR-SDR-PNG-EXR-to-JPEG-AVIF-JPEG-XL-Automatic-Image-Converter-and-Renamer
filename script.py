import os
import subprocess
import argparse
from tkinter import Tk
from tkinter.filedialog import askdirectory
import json


# Function to ask the user for a directory, starting from the script's directory
def select_directory():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    selected_dir = askdirectory(initialdir=script_directory, title="Select the directory containing your images")
    root.destroy()  # Destroy the Tkinter instance after use
    return selected_dir


# Function to load user settings
def load_user_settings():
    if os.path.exists(user_settings_file):
        with open(user_settings_file, 'r') as file:
            user_settings = json.load(file)  # Now 'user_settings' is the dictionary loaded from the JSON
            # Update the default settings with any user-defined settings
            default_settings.update(user_settings)
    return default_settings


# Function to save user settings
def save_user_settings(settings):
    with open(user_settings_file, 'w') as file:
        json.dump(settings, file, indent=4)


# Default processing setting
default_settings = {'prefix': 'Photo ', 'jpeg': 95, 'avif': 99, 'jpegxl': 99}

# Define the path for the user settings file
user_settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_settings.json')

# Load settings (defaults overridden by user settings if they exist)
current_settings = load_user_settings()

# Set up argument parsing
parser = argparse.ArgumentParser(prog="HDR/SDR image convertor and renamer",
                                 description="This program is designed to convert HDR and SDR PNG images into JPEG, AVIF, and JPEG XL codecs. It also renames and organize images into a logical order."
                                 )
parser.add_argument('--prefix', type=str, default=default_settings['prefix'], help=f'Filename prefix for output files (default: "{default_settings["prefix"]}")')
parser.add_argument('--jpeg', type=int, default=default_settings['jpeg'], help=f'Quality setting for JPEG encoding (0 - 100, default: {default_settings["jpeg"]})')
parser.add_argument('--avif', type=int, default=default_settings['avif'], help=f'Quality setting for AVIF encoding (0 - 100, default: {default_settings["avif"]})')
parser.add_argument('--jpegxl', type=int, default=default_settings['jpegxl'], help=f'Quality setting for JPEG XL encoding (0 - 100, default: {default_settings["jpegxl"]})')
# Parse the arguments
parsed_settings = parser.parse_args()
processing_settings = {key: value for key, value in vars(parsed_settings).items()}

# Save the current settings as user defaults if requested
if parsed_settings:
    save_user_settings({
        'prefix': processing_settings['prefix'],
        'jpeg': processing_settings['jpeg'],
        'avif': processing_settings['avif'],
        'jpegxl': processing_settings['jpegxl']
    })

# Specify the working directory containing the files
working_directory = select_directory()

# Get a list of all .png files in the folder
file_list = [file for file in os.listdir(working_directory) if file.endswith('.png')]

# Separate HDR and non-HDR files
non_hdr_files = [filename for filename in file_list if '_HDR' not in filename]
hdr_files = [filename for filename in file_list if '_HDR' in filename]

# Sort files to ensure consistent ordering
non_hdr_files.sort()
hdr_files.sort()

# Determine the number of digits required based on the number of non-HDR files
number_of_files = len(non_hdr_files)
number_of_digits = len(str(number_of_files))

# Enumerate and rename the non-HDR files
for index, filename in enumerate(non_hdr_files):
    # Create the new filename with the correct number of digits
    new_filename = f"{processing_settings['prefix']}{str(index + 1).zfill(number_of_digits)}.png"
    # Create full paths for the rename operation
    src = os.path.join(working_directory, filename)
    dst = os.path.join(working_directory, new_filename)
    # Rename the file
    os.rename(src, dst)

    # Create the corresponding .jpeg, .avif and .jxl files
    png_filename = os.path.join(working_directory,f'{processing_settings["prefix"]}{str(index + 1).zfill(number_of_digits)}')
    command = f'ffmpeg -y -i "{png_filename}.png" -pix_fmt rgb24 "{png_filename}.bmp"'
    subprocess.call(command, shell=True)
    command = f'cjpeg -quality {str(processing_settings["jpeg"])} -optimize -precision 8 -outfile "{png_filename}.jpg" "{png_filename}.bmp"'
    subprocess.call(command, shell=True)
    os.remove(f'{png_filename}.bmp')
    command = f'avifenc --codec aom --speed 6 --qcolor {str(processing_settings["avif"])} --yuv 420 --range full --depth 8 --cicp 1/13/6 --jobs all --ignore-icc --advanced enable-chroma-deltaq=1 "{png_filename}.png" "{png_filename}.avif"'
    subprocess.call(command, shell=True)
    command = f'cjxl "{png_filename}.png" "{png_filename}.jxl" --quality {str(processing_settings["jpegxl"])} --effort 7 --brotli_effort 11 --num_threads -1 --gaborish 1'
    subprocess.call(command, shell=True)

# Enumerate and rename the HDR files
for filename in hdr_files:
    # Extract the base name from the HDR filename
    base_name = filename.split('_HDR')[0]
    print(base_name)
    # Find the index of the base name in the non-HDR list
    base_index = non_hdr_files.index(base_name + '.png') + 1
    # Create the new filename with the correct number of digits
    new_filename_png = f'{processing_settings["prefix"]}{str(base_index).zfill(number_of_digits)}_HDR.png'
    new_filename_exr = f'{processing_settings["prefix"]}{str(base_index).zfill(number_of_digits)}_HDR.exr'
    # Create full paths for the rename operation
    src_png = os.path.join(working_directory, filename)
    src_exr = os.path.join(working_directory, base_name + '_HDR.exr')
    dst_png = os.path.join(working_directory, new_filename_png)
    dst_exr = os.path.join(working_directory, new_filename_exr)
    # Rename the file
    os.rename(src_png, dst_png)
    # Check if the corresponding .exr file exists and rename it
    if os.path.exists(src_exr):
        os.rename(src_exr, dst_exr)

    # Create the corresponding .avif and .jxl files
    png_filename = os.path.join(working_directory,f'{processing_settings["prefix"]}{str(base_index).zfill(number_of_digits)}_HDR')
    command = f'avifenc --codec aom --speed 6 --qcolor {str(processing_settings["avif"])} --yuv 420 --range full --depth 10 --cicp 9/16/9 --jobs all --ignore-icc --advanced enable-chroma-deltaq=1 "{png_filename}.png" "{png_filename}.avif"'
    subprocess.call(command, shell=True)
    command = f'cjxl "{png_filename}.png" "{png_filename}.jxl" --quality {str(processing_settings["jpegxl"])} --effort 7 --brotli_effort 11 --num_threads -1 --gaborish 1 -x color_space=RGB_D65_202_Rel_PeQ'
    subprocess.call(command, shell=True)

