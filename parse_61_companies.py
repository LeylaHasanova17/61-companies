import os
import re
from bs4 import BeautifulSoup

# 1. Folder configuration
# input_folder: the raw filings downloaded from SEC
# output_folder: where the extracted Item 1C sections will be saved
input_folder = "sec_raw_matthew"
output_folder = "extracted_matthew"

print("Starting the extraction of Item 1C sections...")

# 2. Prepare the output directory
# We ensure the folder exists and is empty to avoid mixing data from different runs
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
else:
    for f in os.listdir(output_folder):
        file_to_remove = os.path.join(output_folder, f)
        if os.path.isfile(file_to_remove):
            os.remove(file_to_remove)

def extract_item_1c(text):
    """
    Uses Regex to locate 'Item 1C. Cybersecurity' and captures text until 'Item 2'.
    If 'Item 2' is not found, it captures a fixed buffer of text.
    """
    pattern = re.compile(r'Item\s*1C\.?\s*Cybersecurity', re.IGNORECASE)
    match = pattern.search(text)
    
    if match:
        start_idx = match.start()
        # Look for the start of the next section (usually Item 2)
        next_item = re.compile(r'Item\s*2\.?\s*', re.IGNORECASE)
        end_match = next_item.search(text, start_idx + 20)
        
        if end_match:
            return text[start_idx:end_match.start()]
        
        # Fallback: capture next 20,000 characters if end marker is missing
        return text[start_idx:start_idx + 20000]
    return None

# 3. Main processing loop
if not os.path.exists(input_folder):
    print(f"❌ Error: Input folder '{input_folder}' not found. Please run the download script first.")
    exit()

extracted_count = 0
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".txt") or file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            # Using the Accession Number (folder name) to create a unique filename
            # Format: [AccessionNumber]_[OriginalFileName].txt
            unique_id = os.path.basename(root)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # If file is HTML, strip tags to get clean text for analysis
                if ".html" in file.lower() or "<html" in content.lower()[:500]:
                    soup = BeautifulSoup(content, 'html.parser')
                    content = soup.get_text(separator=' ')

                item_1c_text = extract_item_1c(content)
                
                if item_1c_text:
                    out_name = f"{unique_id}_{file}.txt"
                    with open(os.path.join(output_folder, out_name), 'w', encoding='utf-8') as out_f:
                        out_f.write(item_1c_text)
                    extracted_count += 1
            except Exception as e:
                print(f"Error processing {file}: {e}")

print(f"✅ Success! Extracted {extracted_count} UNIQUE Item 1C sections into '{output_folder}'.")
