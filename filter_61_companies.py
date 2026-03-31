import pandas as pd
import re
import os

# 1. Source filename - we expect this file in the same directory
input_filename = 'matthew_cik.txt'
output_filename = 'matthew_targets.csv'

print("Preparing the target list for SEC download...")

# Check if the input file exists to prevent crashes
if not os.path.exists(input_filename):
    print(f"❌ Error: The file '{input_filename}' was not found.")
    print("Please ensure Matthew's raw CIK list is in this folder.")
    exit()

# 2. Load and clean CIK list (Adding leading zeros for SEC format)
matthew_ciks = []
try:
    with open(input_filename, 'r') as f:
        raw_lines = f.readlines()
        for line in raw_lines:
            # Using regex to find all numeric sequences in each line
            numbers = re.findall(r'\d+', line)
            if numbers:
                # SEC EDGAR requires 10-digit CIKs (zero-padded)
                clean_number = numbers[0].zfill(10)
                matthew_ciks.append(clean_number)
except Exception as e:
    print(f"❌ Error reading the file: {e}")
    exit()

print(f"Total CIKs extracted: {len(matthew_ciks)}")

# 3. Create a clean target DataFrame
# This list will be used by the downloader script
target_df = pd.DataFrame(matthew_ciks, columns=['CIK'])

# 4. Add metadata placeholders
# Real company names will be verified during the SEC download process
target_df['Company Name'] = "Target Company" 
target_df['Form Type'] = "10-K"

# 5. Save as a standardized target list
target_df.to_csv(output_filename, index=False)

print(f"✅ Success! Created '{output_filename}' with {len(target_df)} CIKs.")
print("This CSV is now ready for the 'download_61_companies.py' script.")
