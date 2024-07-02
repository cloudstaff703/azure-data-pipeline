from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

def upload_file(file_path, container_name, blob_name):
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client._get_blob_service_client(blob_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"{file_path}a uploaded to {container_name}/{blob_name} successfully.")

