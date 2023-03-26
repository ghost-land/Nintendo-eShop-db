import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image
import pathlib
from imageconvertor import concatenate_images

import urllib3
urllib3.disable_warnings()

country_codes = ["AE", "AG", "AI", "AN", "AR", "AW", "BB", "BM", "BO", "BR", "BS", "BZ", "CH", "CO", "CR", "CY", "CZ", "DE", "DK", "DM", "DO", "ES", "EE", "FR", "GF", "GP", "GR", "GT", "GY", "HK", "HN", "HU", "IE", "IT", "JM", "JP", "KR", "LC", "LT", "LU", "LV", "MT", "NL", "NO", "NZ", "PA", "PE", "PL", "PT", "RO", "RU", "SA", "SE", "SG", "SI", "SK", "SR", "SV", "TR", "TT", "TW", "US", "UY", "VC", "VE", "VI"]

def format_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = " ".join([word.capitalize() for word in name.split()])
    return name

for country_code in country_codes:
    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?shop_id=1&limit=3000&offset=0"
    try:
        response = requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        continue

    root = ET.fromstring(response.text)
    for content in root.findall(".//content"):
        title_id = content.find(".//title").attrib["id"]
        product_code = content.find(".//product_code").text
        name = content.find(".//name").text
        print(f"title_id: {title_id}, product_code: {product_code}, name: {name}")

        url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=1"
        try:
            response = requests.get(url, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            continue

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
                icon_file = f"{game_directory}/icon_72x72.png"
                open(icon_file, "wb").write(icon_response.content)

                img = Image.open(icon_file)
                img.save(icon_file)

                img = Image.open(icon_file)
                img = img.resize((48, 48))
                img.save(f"{game_directory}/icon_48x48.png")
                root = ET.fromstring(response.text)
                
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
                        upper_image_url = screenshot.find(".//image_url[@type='upper']")
                        lower_image_url = screenshot.find(".//image_url[@type='lower']")
                        if upper_image_url is not None:
                            upper_url = upper_image_url.text
                            response = requests.get(upper_url, verify=False)
                            filename = f"{game_directory}/screenshots/upper_{i+1}.png"
                            open(filename, "wb").write(response.content)
                            if lower_image_url is not None:
                                lower_url = lower_image_url.text
                                response = requests.get(lower_url, verify=False)
                                filename = f"{game_directory}/screenshots/lower_{i+1}.png"
                                open(filename, "wb").write(response.content)
                                if upper_image_url is not None and lower_image_url is not None:
                                    concatenate_images(f"{game_directory}/screenshots/upper_{i+1}.png", f"{game_directory}/screenshots/lower_{i+1}.png", f"{game_directory}/screenshots/screenshot_{i+1}.png")

                  
