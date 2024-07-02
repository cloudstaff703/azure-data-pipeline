import logging
import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request')

    try:
        # Define the health check URL
        heath_check_url = "https://example.com/health"

        # Fetch the health status
        response = requests.get(heath_check_url)
        response.raise_for_status() # Raise an HTTPError for bad responses

        # Process the response
        if response.status_code == 200:
            return func.HttpResponse("Service is up and running", status_code=200)
        else:
            logging.error(f"Service health check failed with status code: {response.status_code}")
            return func.HttpResponse("Service is down", status_code=503)
        
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
        return func.HttpResponse(
            f"Failed to perform health check: {e}"
            status_code=500
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            f"Internal server error: {e}",
            status_code=500
        )