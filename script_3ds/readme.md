# Nintendo eShop 3DS Scraper

The `main.py` script is designed to interact with the Nintendo eShop API for 3DS games. It retrieves information such as game titles, product codes, and images for a specified list of country codes. This README provides instructions on how to use the script and details about its functionality.

## Prerequisites

Before running the script, ensure you have the following dependencies installed:

- Python 3
- `requests`
- `xml.etree.ElementTree`
- `PIL` (Python Imaging Library)
- `imageconvertor` module

Install the required Python packages using:

```bash
pip install requests Pillow
```

## Usage
Open the `main.py` file and update the `country_codes` list with the desired country codes for which you want to retrieve Nintendo eShop data.

Run the script:
```bash
python main.py
```
The script will sequentially retrieve data for each specified country code. It follows these steps:
    - Queries the Nintendo eShop API for a list of titles.
    - Creates directories for each game in the specified country.
    - Downloads XML files containing game information.
    - Downloads and saves icon, banner, thumbnails, and concatenated screenshot images.

The script will create a directory structure under `Nintendo eShop 3DS DB/` for each country code, organized by game titles.

## File Structure
The script generates the following directory structure:

```bash
Nintendo eShop 3DS DB/
|-- Country_Code_1/
|   |-- Game_Name_1/
|   |   |-- game_info.xml
|   |   |-- icon.png
|   |   |-- banner.png
|   |   |-- thumbnails/
|   |   |   |-- thumbnail_1.png
|   |   |   |-- thumbnail_2.png
|   |   |-- screenshots/
|   |   |   |-- screenshot_1.png
|   |   |   |-- screenshot_2.png
|-- Country_Code_2/
...
```
- `game_info.xml`: Contains detailed information about each game.
- `icon.png`: Icon image representing the game.
- `banner.png`: Banner image used for the game.
- `thumbnails/`: Directory containing thumbnail images.
- `screenshots/`: Directory containing concatenated screenshot images.

## imageconvertor.py
The `imageconvertor.py` module provides the `concatenate_images` function, used by `main.py` to combine upper and lower screenshots vertically.

## Important Notes
- **SSL Certificate:** Disable SSL warnings using `urllib3.disable_warnings()` due to potential issues with the Nintendo eShop API SSL certificate.
- **Terms of Use:** Ensure compliance with the terms of use for the Nintendo eShop API when using this script.

Feel free to customize the script according to your requirements. For example, you can modify the `main.py` script to retrieve data for a single country code or to download only specific images.

## Acknowledgments
- [3dbrew](https://www.3dbrew.org/wiki/Nintendo_eShop)
- [3DS Title Database](https://hax0kartik.github.io/3dsdb/)

## Appendix
<details>
  <summary><strong>List of available Country Codes for the 3DS :</strong></summary>

- "AD": Andorra
- "AE": United Arab Emirates
- "AG": Antigua and Barbuda
- "AI": Anguilla
- "AL": Albania
- "AN": Netherlands Antilles (Deprecated)
- "AR": Argentina
- "AT": Austria
- "AU": Australia
- "AW": Aruba
- "AZ": Azerbaijan
- "BA": Bosnia and Herzegovina
- "BB": Barbados
- "BE": Belgium
- "BG": Bulgaria
- "BM": Bermuda
- "BO": Bolivia
- "BR": Brazil
- "BS": Bahamas
- "BW": Botswana
- "BZ": Belize
- "CA": Canada
- "CH": Switzerland
- "CL": Chile
- "CN": China
- "CO": Colombia
- "CR": Costa Rica
- "CY": Cyprus
- "CZ": Czech Republic
- "DE": Germany
- "DJ": Djibouti
- "DK": Denmark
- "DM": Dominica
- "DO": Dominican Republic
- "EC": Ecuador
- "EE": Estonia
- "ER": Eritrea
- "ES": Spain
- "FI": Finland
- "FR": France
- "GB": United Kingdom
- "GD": Grenada
- "GF": French Guiana
- "GG": Guernsey
- "GI": Gibraltar
- "GP": Guadeloupe
- "GR": Greece
- "GT": Guatemala
- "GY": Guyana
- "HK": Hong Kong
- "HN": Honduras
- "HR": Croatia
- "HT": Haiti
- "HU": Hungary
- "IE": Ireland
- "IL": Israel
- "IM": Isle of Man
- "IN": India
- "IS": Iceland
- "IT": Italy
- "JE": Jersey
- "JM": Jamaica
- "JP": Japan
- "KN": Saint Kitts and Nevis
- "KR": South Korea
- "KY": Cayman Islands
- "LC": Saint Lucia
- "LI": Liechtenstein
- "LS": Lesotho
- "LT": Lithuania
- "LU": Luxembourg
- "LV": Latvia
- "MC": Monaco
- "ME": Montenegro
- "MK": North Macedonia
- "ML": Mali
- "MQ": Martinique
- "MR": Mauritania
- "MS": Montserrat
- "MT": Malta
- "MX": Mexico
- "MY": Malaysia
- "MZ": Mozambique
- "NA": Namibia
- "NE": Niger
- "NI": Nicaragua
- "NL": Netherlands
- "NO": Norway
- "NZ": New Zealand
- "PA": Panama
- "PE": Peru
- "PL": Poland
- "PT": Portugal
- "PY": Paraguay
- "RO": Romania
- "RS": Serbia
- "RU": Russia
- "SA": Saudi Arabia
- "SD": Sudan
- "SE": Sweden
- "SG": Singapore
- "SI": Slovenia
- "SK": Slovakia
- "SM": San Marino
- "SO": Somalia
- "SR": Suriname
- "SV": El Salvador
- "SZ": Eswatini
- "TC": Turks and Caicos Islands
- "TD": Chad
- "TR": Turkey
- "TT": Trinidad and Tobago
- "TW": Taiwan
- "US": United States
- "UY": Uruguay
- "VA": Vatican City
- "VC": Saint Vincent and the Grenadines
- "VE": Venezuela
- "VG": British Virgin Islands
- "VI": U.S. Virgin Islands
- "ZA": South Africa
- "ZM": Zambia
- "ZW": Zimbabwe
</details>


## Credits
- [Ghost0159](https://github.com/Ghost0159) for the original script and analysis of Nintendo's CDN.
- [Léon Le Breton](https://github.com/LeonLeBreton) & [22sh](https://twitter.com/0x22sh) for the improvements & more.

For more details, see [commits history](https://github.com/ghost-land/Nintendo-eShop-db/commits/main/script_3ds).


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
