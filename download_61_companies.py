import pandas as pd
import os
from sec_edgar_downloader import Downloader

# 1. SEC Downloader Initialization
# IMPORTANT: SEC requires a valid email for their records. 
# Placeholder used for GitHub; replace with your actual email when running locally.
user_email = "your.email@university.edu" 
company_name = "University of Tulsa Research"

# Using a relative path so it works in any directory
output_path = "sec_raw_matthew"
dl = Downloader(company_name, user_email, output_path)

# 2. Load target CIK list
# Ensure 'matthew_targets.csv' is in the same folder as this script
try:
    targets = pd.read_csv('matthew_targets.csv')
    # Clean and format CIKs to 10 digits
    ciks = targets['CIK'].astype(str).str.zfill(10).tolist()
    print(f"Starting download for {len(ciks)} companies into '{output_path}'...")
except FileNotFoundError:
    print("❌ Error: 'matthew_targets.csv' not found. Please place the CSV in this folder.")
    exit()

# 3. Download 10-K filings (From late 2023 to 2025)
# This captures reports filed after the new SEC Cybersecurity disclosure rule
for cik in ciks:
    try:
        print(f"Checking reports for CIK: {cik}...")
        # Period: October 2023 to March 2026
        dl.get("10-K", cik, after="2023-10-01", before="2026-03-31")
    except Exception as e:
        print(f"Could not download for {cik}: {e}")

print(f"✅ Download process complete. Data saved in '{output_path}'.")
