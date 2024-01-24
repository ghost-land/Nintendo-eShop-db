import requests
import os
from tqdm import tqdm
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import time

MAX_WORKERS = 3  # Maximum number of threads to use

links_req = requests.get("https://web.archive.org/cdx/search/cdx?url=https://kanzashi-movie-wup.cdn.nintendo.net/m/&matchType=prefix&filter=statuscode%3A200&filter=original:.*(.mp4).*&fl=original&collapse=urlkey")
links = links_req.text.splitlines()

if not os.path.exists("mp4"):
    os.mkdir("mp4")
os.chdir("mp4")

def download_file(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    partial_file_name = file_name + ".part"
    print("Processing: " + url)
    
    while True:
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
            break  # Break out of the while loop if download is successful
        except requests.exceptions.RequestException as e:
            print("Error occurred while downloading: " + url)
            print("Error message: " + str(e))
            print("Retrying download...")
            time.sleep(5)  # Wait for 5 seconds before retrying

def resume_download(url, partial_file_name):
    while True:
        try:
            headers = {"Range": "bytes=" + str(os.path.getsize(partial_file_name)) + "-"}
            response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
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
            break  # Break out of the while loop if download is successful
        except requests.exceptions.RequestException as e:
            print("Error occurred while resuming download: " + url)
            print("Error message: " + str(e))
            print("Skipping: " + url)
            break  # Break out of the while loop if download cannot be resumed

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    for link in links:
        url = "http://web.archive.org/web/20220220103440/" + link
        executor.submit(download_file, url)

