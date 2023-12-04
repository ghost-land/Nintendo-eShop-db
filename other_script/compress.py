import os
import shutil
from tqdm import tqdm

# Chemin du dossier à traiter
root_folder = "/home/ghost/Nintendo-eShop-db/script_wiiu/download_wup/wiiu"

# Liste tous les sous-dossiers du dossier racine
subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir()]

# Boucle sur chaque sous-dossier
for subfolder in tqdm(subfolders, desc="Processing folders"):
    # Nom de l'archive à créer
    archive_name = os.path.basename(subfolder)

    # Chemin complet de l'archive
    archive_path = os.path.join(root_folder, archive_name + ".zip")

    # Crée l'archive en compressant le sous-dossier
    shutil.make_archive(archive_name, "zip", subfolder)

    # Supprime le sous-dossier
    shutil.rmtree(subfolder)

    # Renomme l'archive pour enlever l'extension .zip
    os.rename(archive_name + ".zip", archive_path)

    # Affiche le message de progression
    tqdm.write(f"{subfolder} compressed and removed")

