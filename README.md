# azure-data-pipeline
This project demonstrates how to build a data pipeline using Python and various Azure services. The pipeline extracts data from a public API, transforms it, and then loads it into an Azure SQL Database. Azure Functions are used to automate the pipeline, and Azure Storage is used to store raw and processed data.

## Setup Instructions

### Prerequisites

- An active Azure subscription
- Python 3.7 or later
- Azure CLI installed and logged in

### Azure Setup

1. Create a resource group in Azure:
    ```sh
    az group create --name myResourceGroup --location eastus
    ```

2. Create an Azure SQL Database:
    ```sh
    az sql server create --name mySqlServer --resource-group myResourceGroup --location eastus --admin-user myadmin --admin-password mypassword
    az sql db create --resource-group myResourceGroup --server mySqlServer --name myDatabase --service-objective S0
    ```

3. Create a storage account:
    ```sh
    az storage account create --name mystorageaccount --resource-group myResourceGroup --location eastus --sku Standard_LRS
    ```

4. Set up an Azure Function App:
    ```sh
    az functionapp create --resource-group myResourceGroup --consumption-plan-location eastus --runtime python --runtime-version 3.8 --functions-version 3 --name myFunctionApp --storage-account mystorageaccount
    ```

### Local Setup

1. Clone the repository and navigate to the project directory:
    ```sh
    git clone https://github.com/yourusername/azure-data-pipeline.git
    cd azure-data-pipeline
    ```

2. Set up a Python virtual environment and install dependencies:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```sh
    AZURE_STORAGE_CONNECTION_STRING=<your_connection_string>
    SQL_SERVER=<your_sql_server>
    SQL_DATABASE=<your_database>
    SQL_USER=<your_sql_user>
    SQL_PASSWORD=<your_sql_password>
    ```

### Running the Pipeline Locally

1. Extract data:
    ```sh
    python src/extract_data.py
    ```

2. Transform data:
    ```sh
    python src/transform_data.py
    ```

3. Load data:
    ```sh
    python src/load_data.py
    ```

### Deploying to Azure

1. Deploy Azure Functions:
    ```sh
    func azure functionapp publish myFunctionApp
    ```

2. Upload data to Azure Blob Storage:
    ```sh
    python src/upload_to_azure.py
    ```

### CI/CD Pipeline

Set up GitHub Actions workflow to automate testing and deployment of Azure Functions.

**File**: `.github/workflows/ci-cd.yml`