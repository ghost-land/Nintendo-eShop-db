import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image
import pathlib

import urllib3
urllib3.disable_warnings()

country_codes = ["US"]

def format_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = " ".join([word.capitalize() for word in name.split()])
    return name

for country_code in country_codes:
    url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/titles?limit=1000000000"
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

        url = f"https://samurai.ctr.shop.nintendo.net/samurai/ws/{country_code}/title/{title_id}/?shop_id=2"
        print (url)
        try:
            response = requests.get(url, verify=False)
            xml_string = response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            continue

        if product_code.startswith('WUP'):
            game_directory = f"Nintendo eShop WiiU DB/{country_code}/{format_name(name)}"
            ressources_directory = f"{game_directory}/ressources"
            if not os.path.exists(game_directory):
                os.makedirs(game_directory)
                os.makedirs(ressources_directory)
            xml_file = f"{game_directory}/game_info.xml"
            with open(xml_file, "w", encoding="utf-8") as f:
                f.write(response.text)

            icon_url_element = content.find(".//icon_url")
            if icon_url_element is not None:
                icon_url = icon_url_element.text
                icon_response = requests.get(icon_url, verify=False)
                icon_file = f"{ressources_directory}/icon.png"
                open(icon_file, "wb").write(icon_response.content)

                img = Image.open(icon_file)
                img.save(icon_file)

            banner_url_element = content.find(".//banner_url")
            if banner_url_element is not None:
                banner_url = banner_url_element.text
                banner_response = requests.get(banner_url, verify=False)
                banner_file = f"{ressources_directory}/banner.png"
                open(banner_file, "wb").write(banner_response.content)

                img = Image.open(banner_file)
                img.save(banner_file)

            
            screenshots_directory = f"{ressources_directory}/screenshots"
            if not os.path.exists(screenshots_directory):
                os.makedirs(screenshots_directory)
            
            x = ET.fromstring(xml_string)
            i = 0
            for screenshot in x.findall(".//image_url"):
                if screenshot is not None:
                    screenshot_url = screenshot.text
                    screenshot_response = requests.get(screenshot_url, verify=False)
                    screenshot_file = f"{screenshots_directory}/screenshot_{i}.png"
                    open(screenshot_file, "wb").write(screenshot_response.content)
                    i += 1
                else:
                    print("No screenshot found")