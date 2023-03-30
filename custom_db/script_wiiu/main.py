import os
import xml.etree.ElementTree as ET

def generate_xml_files():
    root_dir = './Nintendo eShop WiiU DB/'
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
                        region_xml.append(game_xml)
            xml_string = ET.tostring(region_xml).decode()
            xml_dir = os.path.join('nlib', 'wiiu_db', 'country')
            if not os.path.exists(xml_dir):
                os.makedirs(xml_dir)
            xml_path = os.path.join(xml_dir, region_dir + '.xml')
            with open(xml_path, 'w') as xml_file:
                xml_file.write(xml_string)
            all_xml.append(region_xml)
            print(f"Finished processing {region_dir}!")
    all_xml_string = ET.tostring(all_xml).decode()
    all_xml_dir = os.path.join('nlib', 'wiiu_db')
    if not os.path.exists(all_xml_dir):
        os.makedirs(all_xml_dir)
    all_xml_path = os.path.join(all_xml_dir, 'all_games.xml')
    with open(all_xml_path, 'w') as all_xml_file:
        all_xml_file.write(all_xml_string)

if __name__ == '__main__':
    generate_xml_files()
