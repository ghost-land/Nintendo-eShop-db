import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image
from imageconvertor import concatenate_images
import threading
from io import BytesIO

import urllib3
urllib3.disable_warnings()

country_codes = ["AD", "AE", "AG", "AI", "AL", "AN", "AR", "AT", "AU", "AW", "AZ", "BA", "BB", "BE", "BG", "BM", "BO", "BR", "BS", "BW", "BZ", "CA", "CH", "CL", "CN", "CO", "CR", "CY", "CZ", "DE", "DJ", "DK",
                 "DM", "DO", "EC", "EE", "ER", "ES", "FI", "FR", "GB", "GD", "GF", "GG", "GI", "GP", "GR", "GT", "GY", "HK", "HN", "HR", "HT", "HU", "IE", "IL", "IM", "IN", "IS", "IT", "JE", "JM", "JP", "KN",
                 "KR", "KY", "LC", "LI", "LS", "LT", "LU", "LV", "MC", "ME", "MK", "ML", "MQ", "MR", "MS", "MT", "MX", "MY", "MZ", "NA", "NE", "NI", "NL", "NO", "NZ", "PA", "PE", "PL", "PT", "PY", "RO", "RS",
                 "RU", "SA", "SD", "SE", "SG", "SI", "SK", "SM", "SO", "SR", "SV", "SZ", "TC", "TD", "TR", "TT", "TW", "US", "UY", "VA", "VC", "VE", "VG", "VI", "ZA", "ZM", "ZW"]

# Function that formats the name of the game
def format_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = " ".join([word.capitalize() for word in name.split()])
    return name


# Function that creates xml files and images for a game
def create_game_files(country_code, content):
    title_id = content.find(".//title").attrib["id"]
    product_code = content.find(".//product_code").text
    name = content.find(".//name").text
    print(
        f"Game found : title_id: {title_id}, product_code: {product_code}, name: {name}")

    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=1"
    print(
        f"Retrieving data from {url}")
    goodroot = False
    while goodroot == False:
        try:
            response = requests.get(url, verify=False)
            root = ET.fromstring(response.text)
            goodroot = True
        except (ET.ParseError, requests.exceptions.RequestException) as e:
            print(f"Error : {e} ")

    if product_code.startswith('CTR') or product_code.startswith('KTR') or product_code.startswith('TWL'):
        game_directory = f"Nintendo eShop 3DS DB/{country_code}/{format_name(name)}"
        if not os.path.exists(game_directory):
            os.makedirs(game_directory)
        xml_file = f"{game_directory}/game_info.xml"
        with open(xml_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        icon_url_element = content.find(".//icon_url")
        if icon_url_element is not None:
            icon_url = icon_url_element.text
            icon_response = requests.get(icon_url, verify=False)
            icon_file = f"{game_directory}/icon.png"
            img = Image.open(BytesIO(icon_response.content))
            img.save(icon_file)

            banner_url_element = root.find(".//banner_url")
            if banner_url_element is not None:
                banner_url = banner_url_element.text
                banner_response = requests.get(banner_url, verify=False)
                banner_file = f"{game_directory}/banner.png"
                img = Image.open(BytesIO(banner_response.content))
                img.save(banner_file)
                
            thumbnails = root.findall(".//thumbnails")
            if thumbnails:
                if not os.path.exists(f"{game_directory}/thumbnails"):
                    os.makedirs(f"{game_directory}/thumbnails")
                for th in thumbnails:
                    for i,thumbnail in enumerate(th): 
                        response = requests.get(thumbnail.get('url'), verify=False)
                        filename = f"{game_directory}/thumbnails/thumbnail_{i+1}.png"
                        img = Image.open(BytesIO(response.content))
                        img.save(filename)
                        
            screenshots = root.findall(".//screenshots/screenshot")
            if screenshots:
                if not os.path.exists(f"{game_directory}/screenshots"):
                    os.makedirs(f"{game_directory}/screenshots")
                for i, screenshot in enumerate(screenshots):
                    upper_image_url = screenshot.find(
                        ".//image_url[@type='upper']")
                    lower_image_url = screenshot.find(
                        ".//image_url[@type='lower']")
                    if upper_image_url is not None:
                        upper_url = upper_image_url.text
                        response = requests.get(upper_url, verify=False)
                        upper_image = BytesIO(response.content)
                        if lower_image_url is not None:
                            lower_url = lower_image_url.text
                            response = requests.get(
                                lower_url, verify=False)
                            lower_image = BytesIO(response.content)
                            if upper_image_url is not None and lower_image_url is not None:
                                concatenate_images(upper_image,
                                                   lower_image, f"{game_directory}/screenshots/screenshot_{i+1}.png")


# Function to retrieve data from a country
def get_data_from_country(country_code):
    goodContent = False
    while goodContent == False:
        url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?shop_id=1&limit=3000&offset=0"
        print(
        f"Retrieving data from {url}")
        try:
            response = requests.get(url, verify=False)
            root = ET.fromstring(response.text)
            goodContent = True
        except (requests.exceptions.RequestException, ET.ParseError) as e:
            print(f"Error: {e}")

    for content in root.findall(".//content"):
        create_game_files(country_code, content)


# Function that starts a thread for each country
def main():
    threads = []
    for country_code in country_codes:
        thread = threading.Thread(target=get_data_from_country, args=(country_code,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\n" + "All done!")

if __name__ == "__main__":
    main()