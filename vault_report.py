import pandas as pd
import numpy as np
import json
from datetime import datetime

# Function to convert bytes to TB, GB, MB, KB, or B
def convert_bytes(size_bytes):
    if size_bytes == 0:
        return "0B"
    
    size_name = ("TB", "GB", "MB", "KB", "B")
    # Calculate appropriate unit (TB, GB, MB, KB, B)
    i = int(np.floor(np.log2(size_bytes) / 10))
    # Ensure we don't exceed the list index for the unit
    if i >= len(size_name):
        i = len(size_name) - 1
    # Format the result with appropriate unit
    return f"{size_bytes / (2 ** (i * 10)): .2f}{size_name[i]}"

# Function to convert timestamp
def conv_time(timestamp_ms):
    try:
        timestamp_seconds = timestamp_ms / 1000.0
        dt_object = datetime.utcfromtimestamp(timestamp_seconds)
        formatted_time = dt_object.strftime('%a, %d %b %Y %H:%M:%S +0000')
        return formatted_time
    except Exception as e:
        print("Error occurred:", e)
        return None

# File path for input JSON
input_file_path = 'vault_report.json'

# Read input JSON string from file
with open(input_file_path, 'r') as file:
    input_string = file.read()

# Parse the JSON string
data = json.loads(input_string)

# Convert data to DataFrame
df = pd.json_normalize(data['responseData']['vaults'])

# Convert storage sizes to human-readable format
for column in ['allottedSize', 'usableSize', 'usedPhysicalSizeFromStorage', 
               'usedLogicalSizeFromStorage', 'estimateUsableUsedLogicalSizeFromStorage', 
               'estimateUsableTotalLogicalSizeFromStorage', 'allotmentQuota', 
               'allotmentUsage']:
    df[column] = df[column].apply(convert_bytes)

# Convert timestamp
df['timestamp'] = df['timestamp'].apply(conv_time)

# Save data to CSV
df.to_csv('data.csv', index=False)

# Save data to JSON
df.to_json('data.json', orient='records', indent=4)

print("Data saved to CSV and JSON files.")
