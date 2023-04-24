import requests
import os
from tqdm import tqdm
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 30  # Nombre maximum de threads à utiliser

links_req = requests.get("""https://web.archive.org/cdx/search/cdx?url=https://kanzashi-movie-ctr.cdn.nintendo.net/m/&matchType=prefix&filter=statuscode%3A200&filter=original:.*(.moflex).*&fl=original&collapse=urlkey""")
links = links_req.text.splitlines()

if not os.path.exists("moflex"):
    os.mkdir("moflex")
os.chdir("moflex")

# Fonction pour télécharger un fichier
def download_file(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    print("processing: "+url)
    response = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open(file_name, "wb") as file:
        for data in response.iter_content(chunk_size=1024):
            # Mettre à jour la taille des données téléchargées
            progress_bar.update(len(data))
            # Écrire les données dans le fichier
            file.write(data)
    progress_bar.close()

# Utiliser ThreadPoolExecutor pour télécharger les fichiers en parallèle
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    for link in links:
        url = "http://web.archive.org/web/20220220115806/"+link
        executor.submit(download_file, url)
