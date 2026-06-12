import csv, dotenv, os
from utils.logger import setup_logging

dotenv.load_dotenv()

logger = setup_logging('logs/utils/csv_handler.log')

netbox_url = os.getenv('NETBOX_URL')
netbox_token = os.getenv('NETBOX_V2_TOKEN_RW')

def csv_to_payloads(file_path:str):
    """
    Reads a CSV file and converts its rows into a list of dictionaries.

    Each dictionary represents a row in the CSV file, where the keys are 
    the column headers and the values are the corresponding cell data.

    Args:
        file_path (str): The path to the CSV file to be read.

    Returns:
        list: A list of dictionaries containing the CSV data. 
              Returns an empty list if the file does not exist.
    """

    list_of_values = []
    try:
        logger.info(f"Attempting to read CSV file: {file_path}")
        
        # Safely open the file using a context manager
        with open(file_path, 'r') as csvfile:
            # Use DictReader to automatically map headers to row values
            csv_reader = csv.DictReader(csvfile)

            logger.info(f"Successfully read {len(list_of_values)} rows from {file_path}")

            # Loop through each row and append the dictionary to our list
            for row in csv_reader:
                list_of_values.append(row)
                
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.exception(f"An error occurred while reading the CSV file {file_path}: {e}")

    return list_of_values
        
if __name__ == '__main__':
    list_of_sites = csv_to_payloads('static_inventory/sites/sites.csv')
    print(list_of_sites)


