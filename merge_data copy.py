import pandas as pd
import re
import os

print("Starting the final data merge process...")

# 1. Configuration - Use local filenames for portability
# IMPORTANT: Place your Excel and CSV files in the same folder as this script
matthew_file = '61_companies_2026.xlsx'
analysis_file = 'matthew_analysis_final.csv'
output_file = "Master_Comparison_Table_Final.xlsx"

# 2. Load Matthew's original dataset
# We target the 'Company_facts' sheet as discussed with the team
try:
    if not os.path.exists(matthew_file):
        raise FileNotFoundError(f"'{matthew_file}' not found in the current directory.")

    matthew_df = pd.read_excel(matthew_file, sheet_name='Company_facts')
    
    # Standardize CIK column: removes "CIK " prefix and leading zeros for matching
    matthew_df['CIK_clean'] = matthew_df['CIK'].astype(str).apply(
        lambda x: ''.join(re.findall(r'\d+', x)).lstrip('0')
    )
    print(f"✅ Successfully loaded historical data: {len(matthew_df)} rows.")
except Exception as e:
    print(f"❌ Error reading historical data: {e}")
    exit()

# 3. Load our automated keyword analysis results
try:
    if not os.path.exists(analysis_file):
        raise FileNotFoundError(f"'{analysis_file}' not found. Run analysis script first.")

    leyla_df = pd.read_csv(analysis_file)
    
    # Extract CIK from the automated filename format for merging
    leyla_df['CIK_clean'] = leyla_df['CIK'].astype(str).apply(
        lambda x: str(x).split('-')[0].lstrip('0')
    )
    print(f"✅ Successfully loaded analysis results: {len(leyla_df)} rows.")
except Exception as e:
    print(f"❌ Error reading analysis file: {e}")
    exit()

# 4. Merge datasets (Inner Join)
# This aligns historical breach data with 2024-2025 Item 1C scores
merged_df = pd.merge(matthew_df, leyla_df, on='CIK_clean', how='inner')

# RETAIN FILENAME: Renaming 'Filename' to 'Filing_Source' 
# This allows the Professor to track the specific reporting year (2024 vs 2025)
merged_df = merged_df.rename(columns={'Filename': 'Filing_Source'})

# Data Cleaning: Drop helper columns and fix naming conventions
merged_df = merged_df.drop(columns=['CIK_clean', 'CIK_y'], errors='ignore')
merged_df = merged_df.rename(columns={'CIK_x': 'CIK'}, errors='ignore')

# 5. Export the Final Master Table
try:
    merged_df.to_excel(output_file, index=False)
    print(f"🎉 SUCCESS! Final comparison table created: '{output_file}'")
    print(f"Total matched records: {len(merged_df)}")
except Exception as e:
    print(f"❌ Error exporting to Excel: {e}")
