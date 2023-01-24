import os
import re
import requests
import xml.etree.ElementTree as ET

# List of country codes to download
country_codes = ["US", "AN", "CH", "CO", "ES", "FR", "IT", "JP", "RU"]

def format_name(name):
    # Remove non-alphanumeric characters
    name = re.sub(r"[^\w\s]", '', name)
    # Uppercase the first letter of each word
    name = " ".join([word.capitalize() for word in name.split()])
    return name

# Send request to get list of all games
for country_code in country_codes:
    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?limit=1000000000"
    try:
        response = requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        continue

    # Process XML response
    root = ET.fromstring(response.text)
    for content in root.findall(".//content"):
        title_id = content.find(".//title").attrib["id"]
        product_code = content.find(".//product_code").text
        name = content.find(".//name").text
        print(f"title_id: {title_id}, product_code: {product_code}, name: {name}")

        # Send request to get game details
        url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=1"
        try:
            response = requests.get(url, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            continue

        if product_code.startswith('CTR') or product_code.startswith('KTR'):
            # Create directory to store XML files
            game_directory = f"Nintendo eShop DB/{country_code}/{format_name(name)}"
            if not os.path.exists(game_directory):
                os.makedirs(game_directory)
            # Save XML file as game_info.xml
            xml_file = f"{game_directory}/game_info.xml"
            with open(xml_file, "w", encoding="utf-8") as f:
                f.write(response.text)
