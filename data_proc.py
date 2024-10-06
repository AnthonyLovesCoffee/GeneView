import pandas as pd

# Load the CSV file
file_path = 'OSD-379-samples.csv'
df = pd.read_csv(file_path)

# Function to count occurrences of a string in the 'Sample Name' column
def count_occurrences(sample_string, df):
    # Use the str.contains method to match the string (case insensitive) and count occurrences
    return df['Sample Name'].str.contains(sample_string, case=False).sum()

# List of sample strings to check
sample_strings = [
    'BSL_ISS-T_YNG', 'BSL_ISS-T_OLD', 'BSL_LAR_YNG', 'BSL_LAR_OLD',
    'FLT_ISS-T_YNG', 'FLT_ISS-T_OLD', 'FLT_LAR_YNG', 'FLT_LAR_OLD',
    'GC_ISS-T_YNG', 'GC_ISS-T_OLD', 'GC_LAR_YNG', 'GC_LAR_OLD',
    'VIV_ISS-T_YNG', 'VIV_ISS-T_OLD', 'VIV_LAR_YNG', 'VIV_LAR_OLD'
]

# Initialize an empty dictionary to store counts
occurrences_dict = {}

# Loop through each sample string and count occurrences, storing them in the dictionary
for sample_string in sample_strings:
    occurrences_dict[sample_string] = count_occurrences(sample_string, df)

# Convert the dictionary into a pandas DataFrame
df_occurrences = pd.DataFrame(list(occurrences_dict.items()), columns=['Sample String', 'Occurrences'])

# Display the DataFrame
df_occurrences.to_csv('OSD-379-clean.csv')