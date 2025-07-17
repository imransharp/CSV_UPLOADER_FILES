import csv
import os
import glob
import configparser

def get_latest_csv(folder_path):
    """Finds the latest CSV file in a given folder."""
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        print("❌ No CSV files found in the folder!")
        return None
    latest_file = max(csv_files, key=os.path.getmtime)  # Get most recently modified file
    return latest_file


def split_csv(output_dir, upload_dir, lines_per_file):
    """Automatically detects the latest CSV file and splits it into smaller files."""
    input_file = get_latest_csv(upload_dir)
    if not input_file:
        return  # Exit if no file found
    
    print(f"🔍 Found latest file: {input_file}")

    # output_dir = "D:/Aging_Data_Upload/upload"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Save the header row

        file_count = 1
        output_file_path = os.path.join(output_dir, f'part_{file_count}.csv')
        # output_file = open(f'part_{file_count}.csv', 'w', newline='')
        output_file = open(output_file_path, 'w', newline='', encoding='utf-8')
        writer = csv.writer(output_file)
        writer.writerow(header)  # Write the header to each file

        for i, row in enumerate(reader, start=1):
            writer.writerow(row)
            if i % lines_per_file == 0:  # Close and start a new file
                output_file.close()
                file_count += 1
                output_file_path = os.path.join(output_dir, f'part_{file_count}.csv')
                output_file = open(output_file_path, 'w', newline='', encoding='utf-8')
                # output_file = open(f'part_{file_count}.csv', 'w', newline='')
                writer = csv.writer(output_file)
                writer.writerow(header)

        output_file.close()
        print(f"✅ File split complete! {file_count} parts created in {output_dir}")


config = configparser.ConfigParser()
config.read("config.ini")
UPLOAD_DIR = config["settings"]["upload_dir"]
OUTPUT_DIR = config["settings"]["output_dir"]
# Call the function
split_csv(OUTPUT_DIR, UPLOAD_DIR, 10000)
# change to 5 lakh per file for optimaztion purpose.
# 'D:\\auto_upload_folder\\test.txt'
# D:\ARCHIVE HOW TO DOS\NABIHA KT OF NABIHA IQBAL\Aging Data\26012024
