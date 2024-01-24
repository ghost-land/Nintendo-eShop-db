import requests
import os
from tqdm import tqdm
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 10  # Maximum number of threads to use

links_req = requests.get("https://web.archive.org/cdx/search/cdx?url=https://kanzashi-movie-ctr.cdn.nintendo.net/m/&matchType=prefix&filter=statuscode%3A200&filter=original:.*(.moflex).*&fl=original&collapse=urlkey")
links = links_req.text.splitlines()

if not os.path.exists("moflex"):
    os.mkdir("moflex")
os.chdir("moflex")

def download_file(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    partial_file_name = file_name + ".part"
    print("Processing: " + url)
    try:
        response = requests.get(url, allow_redirects=True, stream=True)
        response.raise_for_status()  # Raise an exception if the response status code is not 200
        total_size = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
        with open(partial_file_name, "ab") as file:
            for data in response.iter_content(chunk_size=1024):
                # Update downloaded data size
                progress_bar.update(len(data))
                # Write data to file
                file.write(data)
        progress_bar.close()
        # Rename the file to remove the ".part" extension once fully downloaded
        os.rename(partial_file_name, file_name)
        print("Download completed: " + url)
    except requests.exceptions.RequestException as e:
        print("Error occurred while downloading: " + url)
        print("Error message: " + str(e))
        print("Resuming download from where it left off...")
        resume_download(url, partial_file_name)

def resume_download(url, partial_file_name):
    try:
        response = requests.get(url, allow_redirects=True, stream=True, headers={"Range": "bytes=" + str(os.path.getsize(partial_file_name)) + "-"})
        response.raise_for_status()  # Raise an exception if the response status code is not 206 (Partial Content)
        total_size = int(response.headers.get("content-length", 0)) + os.path.getsize(partial_file_name)
        progress_bar = tqdm(total=total_size, initial=os.path.getsize(partial_file_name), unit="iB", unit_scale=True)
        with open(partial_file_name, "ab") as file:
            for data in response.iter_content(chunk_size=1024):
                # Update downloaded data size
                progress_bar.update(len(data))
                # Write data to file
                file.write(data)
        progress_bar.close()
        # Rename the file to remove the ".part" extension once fully downloaded
        os.rename(partial_file_name, os.path.basename(partial_file_name))
        print("Download resumed and completed: " + url)
    except requests.exceptions.RequestException as e:
        print("Error occurred while resuming download: " + url)
        print("Error message: " + str(e))

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    for link in links:
        url = "http://web.archive.org/web/20220220115806/" + link
        executor.submit(download_file, url)
