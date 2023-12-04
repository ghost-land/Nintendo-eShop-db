# MOFLEX Downloader

The `download_moflex.py` script is designed to download MOFLEX files from a specific URL. It utilizes multithreading to download files in parallel for faster performance.

## Prerequisites
Before running the script, ensure you have the following dependencies installed:

- Python 3
- `requests`
- `tqdm`
- `urllib.parse`
- `concurrent.futures.ThreadPoolExecutor`

Install the required Python packages using:

```bash
pip install requests tqdm
```

## Usage
Run the script:
```bash
python download_moflex.py
```
The script will retrieve MOFLEX files from the specified URL using multiple threads for efficient downloading.

## File Structure
The script generates the following directory structure:
```bash
moflex/
|-- downloaded_file_1.moflex
|-- downloaded_file_2.moflex
|-- ...
```

## Configuration
Adjust the following parameters in the script according to your needs:

- `MAX_WORKERS`: Maximum number of threads to use for parallel downloads.


## Important Notes
- **URL:** The script uses a specific URL to fetch MOFLEX files. Ensure the URL is up-to-date and valid.
- **SSL Certificate:** No SSL certificate warnings are disabled in the script, similar to the original Nintendo eShop scraper script.

Feel free to customize the script according to your requirements. For example, you can modify the script to download files from a different URL or make other adjustments as needed.


## Credits
- Original script by [Léon Le Breton](https://github.com/LeonLeBreton)
- Additional improvements by [Ghost0159](https://github.com/Ghost0159/)

For more details, see [commits history](https://github.com/ghost-land/Nintendo-eShop-db/commits/main/script_3ds/videos).


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
