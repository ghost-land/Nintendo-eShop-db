import requests
import logging
import colorlog
from datetime import datetime

# Set up logging configuration
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(message)s',
    datefmt='%H:%M:%S'))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def fetch_json_data(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Successfully fetched the JSON data
            return response.json()
        else:
            # Failed to fetch JSON data
            logger.error("Error fetching JSON data. Status code: %d", response.status_code)
            return None
    except Exception as e:
        logger.error("Error fetching JSON data: %s", str(e))
        return None

def group_title_ids_by_region(data):
    title_ids_by_region = {}

    # Iterate through each entry in the JSON data
    for entry in data:
        title_id = entry["titleID"]
        region = entry["region"]

        # Group title IDs by region
        if region not in title_ids_by_region:
            title_ids_by_region[region] = []

        title_ids_by_region[region].append(title_id)

    return title_ids_by_region

def generate_commands(title_ids_by_region):
    # Generate commands for each region
    for region, title_ids in title_ids_by_region.items():
        command = f"Region = {region} --> python3 FunKiiU.py -title {' '.join(title_ids)} -onlinekeys"
        with open('commands.log', 'a') as file:
            file.write(command + "\n")

def main():
    url = "https://dev.ghosteshop.com/titleKeys.json"
    
    # Log script start
    logger.info("Script started at %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Fetch JSON data
    data = fetch_json_data(url)

    if data:
        # Group title IDs by region
        title_ids_by_region = group_title_ids_by_region(data)

        # Generate and write commands to a file
        generate_commands(title_ids_by_region)

        # Log script end
        logger.info("Script completed successfully at %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logger.info("Commands have been successfully generated and written to commands.log")

if __name__ == "__main__":
    main()
