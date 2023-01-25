import os
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image

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

            # download icon
            icon_url_element = content.find(".//icon_url")
            if icon_url_element is not None:
                icon_url = icon_url_element.text
                icon_response = requests.get(icon_url, verify=False)
                icon_file = f"{game_directory}/icon_72x72.png"
                open(icon_file, "wb").write(icon_response.content)

                # convert to png
                img = Image.open(icon_file)
                img.save(icon_file)

                # resize the image to 48x48
                img = Image.open(icon_file)
                img = img.resize((48, 48))
                img.save(f"{game_directory}/icon_48x48.png")


                root = ET.fromstring(response.text)
                screenshots = root.findall(".//screenshots/screenshot")
                if screenshots:
                    if not os.path.exists(f"{game_directory}/screenshots"):
                        os.makedirs(f"{game_directory}/screenshots")
                    for i, screenshot in enumerate(screenshots):
                        for url_type in ["upper", "lower"]:
                            url = screenshot.find(f".//image_url[@type='{url_type}']").text
                            response = requests.get(url, verify=False)
                            filename = f"{game_directory}/screenshots/{url_type}_{i+1}.jpg"
                            open(filename, "wb").write(response.content)

