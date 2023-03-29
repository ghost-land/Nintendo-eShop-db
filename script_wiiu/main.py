import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image
import threading
import urllib3
import pathlib
from io import BytesIO
# Disable SSL certificate warnings
urllib3.disable_warnings()

# Countries to process
country_codes = ["AD", "AE", "AG", "AI", "AL", "AN", "AR", "AT", "AU", "AW", "AZ", "BA", "BB", "BE", "BG", "BM", "BO", "BR", "BS", "BW", "BZ", "CA", "CH", "CL", "CN", "CO", "CR", "CY", "CZ", "DE", "DJ", "DK",
                 "DM", "DO", "EC", "EE", "ER", "ES", "FI", "FR", "GB", "GD", "GF", "GG", "GI", "GP", "GR", "GT", "GY", "HK", "HN", "HR", "HT", "HU", "IE", "IL", "IM", "IN", "IS", "IT", "JE", "JM", "JP", "KN",
                 "KR", "KY", "LC", "LI", "LS", "LT", "LU", "LV", "MC", "ME", "MK", "ML", "MQ", "MR", "MS", "MT", "MX", "MY", "MZ", "NA", "NE", "NI", "NL", "NO", "NZ", "PA", "PE", "PL", "PT", "PY", "RO", "RS",
                 "RU", "SA", "SD", "SE", "SG", "SI", "SK", "SM", "SO", "SR", "SV", "SZ", "TC", "TD", "TR", "TT", "TW", "US", "UY", "VA", "VC", "VE", "VG", "VI", "ZA", "ZM", "ZW"]

# Function to format the name of a game
def format_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = " ".join([word.capitalize() for word in name.split()])
    return name

# Function to download an image and save it to disk
def download_image(url, filename):
    try:
        response = requests.get(url, verify=False)
        img = Image.open(BytesIO(response.content))
        img.save(filename)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Function to process a game
def process_game(country_code, content):
    title_id = content.find(".//title").attrib["id"]
    product_code = content.find(".//product_code").text
    name = content.find(".//name").text

    print(f"Game found : title_id: {title_id}, product_code: {product_code}, name: {name}")

    # Download the game information in XML
    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=2"
    print(
        f"Retrieving data from {url}")
    try:
        response = requests.get(url, verify=False)
        xml_string = response.text
        root = ET.fromstring(xml_string)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    # If the product is a Wii U game, download the resources (images)
    if product_code.startswith('WUP'):
        game_directory = f"Nintendo eShop WiiU DB/{country_code}/{format_name(name)}"
        ressources_directory = f"{game_directory}/ressources"

        try:
            # Create directories for images and XML
            pathlib.Path(ressources_directory).mkdir(parents=True, exist_ok=True)

            # Save game information in XML
            xml_file = f"{game_directory}/game_info.xml"
            with open(xml_file, "w", encoding="utf-8") as f:
                f.write(response.text)

            # Download and save the icon
            icon_url_element = content.find(".//icon_url")
            if icon_url_element is not None:
                icon_url = icon_url_element.text
                icon_file = f"{ressources_directory}/icon.png"
                download_image(icon_url, icon_file)

            # Download and save the banner
            banner_url_element = content.find(".//banner_url")
            if banner_url_element is not None:
                banner_url = banner_url_element.text
                banner_file = f"{ressources_directory}/banner.png"
                download_image(banner_url, banner_file)

            # Download and save screenshots
            for i, screenshot in enumerate(root.findall(".//image_url")):
                screenshots_directory = f"{game_directory}/screenshots"
                if not os.path.exists(screenshots_directory):
                    os.makedirs(screenshots_directory)

                if screenshot is not None:
                    screenshots_directory = f"{game_directory}/screenshots"
                    screenshot_url = screenshot.text
                    screenshot_file = f"{screenshots_directory}/screenshot_{i+1}.png"
                    download_image(screenshot_url, screenshot_file)
                else:
                    print("No screenshot found")
        except Exception as e:
            print(f"Error processing game {title_id}: {e}")

        print(f"Game {title_id} processed successfully")

# Function to retrieve the list of games for a given country
def get_games(country_code):
    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?shop_id=2&limit=3000&offset=0"
    print(
        f"Retrieving data from {url}")
    try:
        response = requests.get(url, verify=False)
        xml_string = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    root = ET.fromstring(xml_string)
    games = root.findall(".//content")
    return games
    
# Main function
def main():
    # Process each country in a separate thread
    for country_code in country_codes:
        games = get_games(country_code)
        threads = []
        for content in games:
            t = threading.Thread(target=process_game, args=(country_code, content))
            threads.append(t)
            t.start()
    
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
