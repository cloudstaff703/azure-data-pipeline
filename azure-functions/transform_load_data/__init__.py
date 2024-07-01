import logging
import pandas as pd
import pyodbc
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function started processing')

    connection_string = os.environ["AzureWebJobsStorage"]
    container_name = "data"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client("raw_data.json")
    raw_data = json.loads(blob_client.download_blob().readall())

    df = pd.json_normalize(raw_data['entries'])
    df = df.dropna()

    blob_client = container_client.get_blob_client("transformed_data.csv")
    blob_client.upload_blob(df.to_csv(index=False), overwrite=True)

    server = os.environ['SQL_SERVER']
    database = os.environ['SQL_DATABASE']
    username = os.environ['SQL_USER']
    password = os.environ['SQL_PASSWORD']
    connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = connection.cursor()

    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Data' and xtype='U')
        CREATE TABLE Data (
            
        )
    ''')

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO Data (API, Description, Auth, HTTPS, Cors, Link, Category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       row['API'], row['Description'], row['Auth'], row['HTTPS'], row['Cors'], row['Link'], row['Category'])
        
    connection.commit()
    cursor.close()
    connection.close()
    logging.info('Data successfully transformed and loaded into the database')