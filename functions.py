#  various functions used by the server to process and output the incoming files

from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def extract_datetime(file_path):
    """
    Receives a file path to an image and returns the exif date from metadata
    originally developed by Eric Mitchell @mitch1625 for CS361 group project Summer 2025 OSU
    """
    try:
        img = Image.open(file_path)
        exif_data = img.getexif()
        for tagid in exif_data:
          tag_name = TAGS.get(tagid, tagid)
          if tag_name == 'DateTime':
            date_value = exif_data.get(tagid)  # DateTime value
            date_raw = datetime.strptime(date_value, "%Y:%m:%d %H:%M:%S")  # Remove the time
            formatted_date = date_raw.strftime("%Y-%m-%d")  # Format the date
            img.close()
            return formatted_date
        img.close()
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return 0