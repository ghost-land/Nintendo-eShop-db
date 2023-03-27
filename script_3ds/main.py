import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image
import pathlib
from imageconvertor import concatenate_images
import threading
import time

import urllib3
urllib3.disable_warnings()

country_codes = ["AE", "AG", "AI", "AN", "AR", "AW", "BB", "BM", "BO", "BR", "BS", "BZ", "CH", "CO", "CR", "CY", "CZ", "DE", "DK", "DM", "DO", "ES", "EE", "FR", "GF", "GP", "GR", "GT", "GY", "HK", "HN", "HU",
                 "IE", "IT", "JM", "JP", "KR", "LC", "LT", "LU", "LV", "MT", "NL", "NO", "NZ", "PA", "PE", "PL", "PT", "RO", "RU", "SA", "SE", "SG", "SI", "SK", "SR", "SV", "TR", "TT", "TW", "US", "UY", "VC", "VE", "VI"]

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
        f"title_id: {title_id}, product_code: {product_code}, name: {name}")

    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=1"
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
            open(icon_file, "wb").write(icon_response.content)

            img = Image.open(icon_file)
            img.save(icon_file)

            banner_url_element = root.find(".//banner_url")
            if banner_url_element is not None:
                banner_url = banner_url_element.text
                banner_response = requests.get(banner_url, verify=False)
                banner_file = f"{game_directory}/banner.png"
                open(banner_file, "wb").write(banner_response.content)
                img = Image.open(banner_file)
                img.save(banner_file)

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
                        filename = f"{game_directory}/screenshots/upper_{i+1}.png"
                        open(filename, "wb").write(response.content)
                        if lower_image_url is not None:
                            lower_url = lower_image_url.text
                            response = requests.get(
                                lower_url, verify=False)
                            filename = f"{game_directory}/screenshots/lower_{i+1}.png"
                            open(filename, "wb").write(response.content)
                            if upper_image_url is not None and lower_image_url is not None:
                                concatenate_images(f"{game_directory}/screenshots/upper_{i+1}.png",
                                                   f"{game_directory}/screenshots/lower_{i+1}.png", f"{game_directory}/screenshots/screenshot_{i+1}.png")


# Function to retrieve data from a country
def get_data_from_country(country_code):
    goodContent = False
    while goodContent == False:
        url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?shop_id=1&limit=3000&offset=0"
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

    # Creation of the file all_xml.xml
    all_xml_file = 'all_xml.xml'
    root = ET.Element('games')
    for country_code in country_codes:
        for folderName, subfolders, filenames in os.walk(f"Nintendo eShop 3DS DB/{country_code}"):
            for filename in filenames:
                if filename == 'game_info.xml':
                    game_info_file = os.path.join(folderName, filename)
                    game_info_root = ET.parse(game_info_file).getroot()
                    
                    game = ET.SubElement(root, 'game')

                    title_id = game_info_root.find('.//title').attrib['id']
                    product_code = game_info_root.find('.//product_code').text
                    region = country_code
                    name = game_info_root.find('.//name').text
                    plateform_name = game_info_root.find('.//plateform_name').text
                    release_date = game_info_root.find('.//release_date').text
                    selling_price = game_info_root.find('.//selling_price').text
                    publisher = game_info_root.find('.//publisher').text
                    description = game_info_root.find('.//description').text
                    age_rating = game_info_root.find('.//age_rating').text
                    genre = game_info_root.find('.//genre').text
                    players = game_info_root.find('.//players').text
                    compatible_controllers = game_info_root.find('.//compatible_controllers').text
                    official_website = game_info_root.find('.//official_website').text
                    copyright = game_info_root.find('.//copyright').text

                    ET.SubElement(game, 'title_id').text = title_id
                    ET.SubElement(game, 'product_code').text = product_code
                    ET.SubElement(game, 'region').text = region
                    ET.SubElement(game, 'name').text = name
                    ET.SubElement(game, 'plateform_name').text = plateform_name
                    ET.SubElement(game, 'release_date').text = release_date
                    ET.SubElement(game, 'selling_price').text = selling_price
                    ET.SubElement(game, 'publisher').text = publisher
                    ET.SubElement(game, 'description').text = description
                    ET.SubElement(game, 'age_rating').text = age_rating
                    ET.SubElement(game, 'genre').text = genre
                    ET.SubElement(game, 'players').text = players
                    ET.SubElement(game, 'compatible_controllers').text = compatible_controllers
                    ET.SubElement(game, 'official_website').text = official_website
                    ET.SubElement(game, 'copyright').text = copyright

    # Creation of the all_xml folder
    all_xml_directory = 'all_xml'
    if not os.path.exists(all_xml_directory):
        os.makedirs(all_xml_directory)
    # Save the all_xml file
    ET.ElementTree(root).write(os.path.join(all_xml_directory, all_xml_file))

    print("Done")


if __name__ == "__main__":
    main()