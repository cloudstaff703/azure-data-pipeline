import pandas as pd
import json

# Load the raw data
with open("data/raw_data.json", "r") as file:
    data = json.load(file)

# Convert to DataFrame for transformation
df = pd.json_normalize(data['drinks'])
print(df)

# Perform data cleaning and transformation
# df = df.dropna() # Example transformation: drop missing values

# Save the transformed data to a CSV file
df.to_csv("data/transformed_data.csv", index=False)