import os
import pandas as pd

# 1. Define the cybersecurity keywords based on the research criteria
# These terms are searched within Item 1C sections to score disclosure depth
keywords = {
    'Security_Training': ['training', 'awareness', 'education'],
    'MFA': ['mfa', 'multi-factor', 'two-factor', '2fa'],
    'Phishing': ['phishing', 'social engineering'],
    'Incident_Response': ['incident response', 'remediation', 'recovery'],
    'Third_Party_Risk': ['third-party', 'vendor', 'supply chain']
}

# Folder containing the extracted text files from SEC filings
input_folder = "extracted_matthew"
results = []

# Check if the input directory exists to prevent errors for other users
if not os.path.exists(input_folder):
    print(f"❌ Error: The folder '{input_folder}' was not found.")
    print("Please run the parsing script first to generate extracted text files.")
    exit()

files_to_analyze = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
print(f"Analyzing {len(files_to_analyze)} files...")

# 2. Iterate through each extracted Item 1C file
for file in files_to_analyze:
    file_path = os.path.join(input_folder, file)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        # Extract CIK from filename (format: CIK_accessionnumber.txt)
        cik = file.split('_')[0]
        
        # Initialize scoring dictionary for this specific filing
        file_results = {'CIK': cik, 'Filename': file}
        
        # 3. Keyword matching logic (binary scoring: 1 if found, 0 if not)
        for category, terms in keywords.items():
            found = 0
            for term in terms:
                if term in content:
                    found = 1
                    break
            file_results[category] = found
            
        results.append(file_results)
    except Exception as e:
        print(f"Could not process file {file}: {e}")

# 4. Save the finalized analysis to a CSV file
df_results = pd.DataFrame(results)
output_file = "matthew_analysis_final.csv"
df_results.to_csv(output_file, index=False)

print(f"✅ Keyword analysis complete! Results saved to '{output_file}'.")
