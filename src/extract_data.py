import requests
import json

# Define the API endpoint and parameters
api_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita"
response = requests.get(api_url)

# check for a successful response
if response.status_code == 200:
    data = response.json()
    # Save the raw data to a local file
    with open("data/raw_data.json", "w") as file:
        json.dump(data, file)
else:
    print("Failed to fetch data:", response.status_code)