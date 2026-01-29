#  various functions used by the server to process and output the incoming files

from PIL import Image
from PIL.ExifTags import TAGS
import csv
import os
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

def date_to_epoch(date_string: str) -> float:
    """Receives a date string in mm-dd-yyyy format and returns that date in epoch time"""
    date_strings = date_string.split('-')
    year = int(date_strings[0])
    month = int(date_strings[1])
    day = int(date_strings[2])
    date_obj = datetime(year, month, day, 0, 0, 0)

    return date_obj.timestamp()

def date_rewrite(date: str, filepath: str):
    """Receives a date string and a filepath and modifies the timestamp on the image file to reflect that date"""
    epoch_time = date_to_epoch(date)
    os.utime(filepath, (epoch_time, epoch_time))
    return True

def spreadsheet_writer(date: str, vendor: str, amount: str, category: str):
    """Receives a date, vendor, amount, and category and writes it as a new row in spreadsheet/receipts.csv"""
    #  check if spreadsheet/receipts.csv exists, if not, create it with header row
    if not os.path.exists('spreadsheet/receipts.csv'):
        with open(f'spreadsheet/receipts.csv', 'w', newline='') as initial_spreadsheet:
            initial_writer = csv.writer(initial_spreadsheet)
            initial_writer.writerow(['Date', 'Vendor', 'Amount', 'Category'])
        initial_spreadsheet.close()

    # write new data to receipts.csv
    with open(f'spreadsheet/receipts.csv', 'a', newline='') as spreadsheet:
        writer = csv.writer(spreadsheet)
        writer.writerow([date, vendor, amount, category])
    spreadsheet.close()

    return True
