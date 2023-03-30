import os
import xml.etree.ElementTree as ET
import urllib.parse

def generate_xml_files():
    root_dir = './Nintendo eShop 3DS DB/'
    all_xml = ET.Element('all_games')
    for region_dir in os.listdir(root_dir):
        region_path = os.path.join(root_dir, region_dir)
        if os.path.isdir(region_path):
            print(f"Processing region {region_dir}...")
            region_xml = ET.Element('region')
            region_xml.set('name', region_dir)
            for game_dir in os.listdir(region_path):
                game_path = os.path.join(region_path, game_dir)
                if os.path.isdir(game_path):
                    game_xml_path = os.path.join(game_path, 'game_info.xml')
                    if os.path.exists(game_xml_path):
                        print(f"  Adding {game_xml_path} to {region_dir}.xml...")
                        game_xml = ET.parse(game_xml_path).getroot()
                        # replace icon URL
                        icon_path = os.path.join(game_path, 'icon.png')
                        icon_url_path = os.path.relpath(icon_path, './Nintendo eShop 3DS DB/').replace('\\', '/')
                        icon_url = 'https://cdn.ghosteshop.com/db/3ds/' + urllib.parse.quote(icon_url_path)
                        for icon_url_element in game_xml.findall('.//icon_url'):
                            icon_url_element.text = icon_url
                        # replace banner URL
                        banner_path = os.path.join(game_path, 'banner.png')
                        banner_url_path = os.path.relpath(banner_path, './Nintendo eShop 3DS DB/').replace('\\', '/')
                        banner_url = 'https://cdn.ghosteshop.com/db/3ds/' + urllib.parse.quote(banner_url_path)
                        for banner_url_element in game_xml.findall('.//banner_url'):
                            banner_url_element.text = banner_url
                        region_xml.append(game_xml)
            xml_string = ET.tostring(region_xml).decode()
            xml_dir = os.path.join('nlib', '3ds_db', 'country')
            if not os.path.exists(xml_dir):
                os.makedirs(xml_dir)
            xml_path = os.path.join(xml_dir, region_dir + '.xml')
            with open(xml_path, 'w') as xml_file:
                xml_file.write(xml_string)
            all_xml.append(region_xml)
            print(f"Finished processing {region_dir}!")
    all_xml_string = ET.tostring(all_xml).decode()
    all_xml_dir = os.path.join('nlib', '3ds_db')
    if not os.path.exists(all_xml_dir):
        os.makedirs(all_xml_dir)
    all_xml_path = os.path.join(all_xml_dir, 'all_games.xml')
    with open(all_xml_path, 'w') as all_xml_file:
        all_xml_file.write(all_xml_string)

if __name__ == '__main__':
    generate_xml_files()
