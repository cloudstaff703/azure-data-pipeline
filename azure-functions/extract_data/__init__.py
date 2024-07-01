import logging
import requests
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request')

    api_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        connection_string = os.environ["AzureWebJobsStorage"]
        container_name = "data"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        blob_client = container_client.get_blob_client("raw_data.json")
        blob_client.upload_blob(json.dumps(data), overwrite=True)
        return func.HttpResponse(f"Data successfully extracted and stored.")
        
    else:
        return func.HttpResponse(f"Failed to fetch data: {response.status_code}", status_code=500)
