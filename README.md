# TrueHDR/SDR PNG/EXR to JPEG/AVIF/JPEG XL Automatic Image Converter and Renamer

## Overview

This script is designed to automate the process of converting SDR PNG images exported from Lightroom and HDR PNG images exported from Photoshop into various image formats such as JPEG, AVIF, and JPEG XL for SDR and AVIF and JPEG XL for HDR. It also renames and organizes these images into a logical and sequential order, together with HDR EXR images exported from Photoshop.

## Motivation

As a photographer excited for latest technologies, Sometimes, you may find JPEG insufficient in terms of compression artifacts in dark areas even in the best encoding quality, and flexibility in HDR details preservation. When I finish photo postprocessing in Lightroom and Photoshop, I export all images as SDR PNGs from Lightroom and some images, which might look astonishing in HDR, I export in HDR PNGs and HDR EXRs from Photoshop. I might end up with something like DSC4852.png (SDR), DSC4854_HDR.png, DSC4854_HDR.exr, and so on. Everybody like to have photos oraganized, but batch renamers dont't deliver the best output when it comes to determining filename together with _HDR suffix and multiple extensions and manual organizing can be time-consuming, especially when dealing with large batches of images. So I created this script, which will simplify and automate the conversion and renaming process, saving time and reducing the potential for errors, and you can focus on what you love - capturing more stunning images with the latest tools at your disposal.

## Features

- **Automatic Renaming:** The script renames images with a user-defined prefix and ensures consistent numbering, even across HDR and SDR images.
- **Format Conversion:** Converts images to JPEG, AVIF, and JPEG XL formats using configurable quality settings.
- **HDR Support:** Handles HDR images by renaming associated `_HDR.png` and `_HDR.exr` files and converting them with appropriate settings.
- **User Settings:** Allows users to save their preferred settings, which can be automatically loaded in future runs.
- **Interactive Directory Selection:** The script prompts the user to select the directory containing images, starting from the last used directory or the script's directory if no previous selection exists.

## Prerequisites

Before running the script, make sure you have the following tools installed:

- **Python 3.x:** Ensure Python is installed and added to your system's PATH.
- **ffmpeg:** Required for image conversion. Make sure ffmpeg is installed and accessible from the command line.
- **cjpeg:** A utility from the `libjpeg-turbo` package, used for converting images to JPEG format.
- **avifenc:** Part of the `libavif` tools, used for encoding AVIF images.
- **cjxl:** Part of the `libjxl` reference implementation, used for encoding JPEG XL images.


## Installation

1. Clone or Download the Script

2. Ensure all prerequisites are installed and accessible from your command line. 

3. Navigate to the directory containing the script and run it using Python  

```bash
cd path/to/your/script
python script.py
```

## Usage

### Command-Line Usage

You can run the script from the command line with customizable arguments. The script supports the following options:

- `--prefix`: Filename prefix for output files (default: `"Photo "`)
- `--jpeg`: Quality setting for JPEG encoding (0 - 100, default: `95`)
- `--avif`: Quality setting for AVIF encoding (0 - 100, default: `99`)
- `--jpegxl`: Quality setting for JPEG XL encoding (0 - 100, default: `99`)

**Example:**

```bash
python script.py --prefix "Photo " --jpeg 95 --avif 99 --jpegxl 99
```

### Running from Explorer ###
You can run the script directly from Explorer by double-clicking on it.

### Directory Selection ###
When the script is executed, it will prompt you to select the directory containing your images. By default, it will start in the directory where the script is located.

### Saving User Settings ###
If you ran the script from command lite, your user setting will be stored in `user_settings.json` file inside script's directory. These settings will be loaded automatically the next time you run the script, if you don't enter new ones.


## References

- [ffmpeg](https://www.ffmpeg.org/) v7.0-full
- [libjpeg-turbo](https://libjpeg-turbo.org/) v3.0.3-vc64
- [libavif](https://github.com/AOMediaCodec/libavif) v1.1.1 x64
- [libjxl](https://github.com/libjxl/libjxl) v0.10.3 x64

## License

I hope that this script will help you to make your images easily organized and available in HDR formats.

Feel free to use and update its functionality by your desired needs.