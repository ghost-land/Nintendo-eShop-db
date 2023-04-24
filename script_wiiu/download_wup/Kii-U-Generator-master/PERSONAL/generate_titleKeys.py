import requests
import json
from bs4 import BeautifulSoup
import subprocess
import logging
logging.basicConfig(level=logging.INFO)
import threading

# Récupération de la page
url = 'http://wiiubrew.org/wiki/Title_database'
logging.info('Récupération de la page')
response = requests.get(url)

# Extraction des données de la page
soup = BeautifulSoup(response.text, 'html.parser')
table_data = soup.find_all('table')

# Fonction pour récupérer la titlekey
def get_title_key(title_id):
    output = subprocess.check_output('python C:\\Users\\Ghost0159\\Downloads\\Kii-U-Generator-master\\Kii-U-Generator-master\\keygen.py {}'.format(title_id), shell=True, encoding='utf-8')
    titleKey = output.split("\n")[-2].split(" ")[-1]
    print('titleKey trouvé pour le titleID : ' + title_id + ' est : ' + titleKey)
    return titleKey

# Création des threads
threads = []

# Création du dictionnaire
data = {}

for table in table_data:
    table_rows = table.find_all('tr')

    # Récupération des attributs
    table_header = table_rows[0].find_all('th')
    attributes = [th.text.strip() for th in table_header]
    attributes.append('titleKey')
    logging.info('Récupération des attributs')

    # Récupération des valeurs
    for tr in table_rows[1:]:
        table_data = tr.find_all('td')
        values = [td.text.strip() for td in table_data]
        # Suppression des tirets dans le titlleID
        title_id = values[0].replace('-', '')
        logging.info('Suppression des tirets dans le titlleID')

        # Création du dictionnaire
        data[title_id] = {}
        for i in range(len(attributes)-1):
            data[title_id][attributes[i]] = values[i]

        # Création du thread
        thread = threading.Thread(target=get_title_key, args=(title_id,))
        threads.append(thread)

# Exécution des threads
for thread in threads:
    thread.start()

# Attente des threads
for thread in threads:
    thread.join()

# Ajout des titleKeys
for title_id in data.keys():
    data[title_id]['titleKey'] = get_title_key(title_id)

# Conversion en JSON
logging.info('Conversion en JSON')
with open('titleKeys.json', 'w', encoding='utf-8') as outfile:  
    json.dump(data, outfile)

# Formatage du JSON
logging.info('Formatage du JSON')
formated_data = []
for title_id, value in data.items():
    formated_data.append({"titleID": title_id, "titleKey": value['titleKey'], "name": value['Description'], "region": value['Region'], "ticket": "1"})

# Écriture du fichier
with open('formated_titleKeys.json', 'w') as outfile:  
    json.dump(formated_data, outfile)

# Création de la page web
logging.info('Création de la page web')

# En-tête HTML
html = '<!DOCTYPE html>'
html += '<html>'
html += '<head>'
html += '<title>Title Keys Wii U</title>'
html += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
html += '<style>'
html += 'table {'
html += 'width: 100%;'
html += 'border-collapse: collapse;'
html += '}'
html += 'table th {'
html += 'border: 1px solid #000000;'
html += 'padding: 5px 10px;'
html += '}'
html += 'table td {'
html += 'border: 1px solid #000000;'
html += 'padding: 5px 10px;'
html += '}'
html += '</style>'
html += '</head>'
html += '<body>'
html += '<h1>Title Keys Wii U</h1>'
html += '<table>'
html += '<thead>'
html += '<tr>'
html += '<th>TitleID</th>'
html += '<th>Title Key</th>'
html += '<th>Name</th>'
html += '<th>Region</th>'
html += '<th>Ticket</th>'
html += '</tr>'
html += '</thead>'
html += '<tbody>'

# Remplissage des données
for entry in formated_data:
    html += '<tr>'
    html += '<td>{}</td>'.format(entry['titleID'])
    html += '<td>{}</td>'.format(entry['titleKey'])
    html += '<td>{}</td>'.format(entry['name'])
    html += '<td>{}</td>'.format(entry['region'])
    html += '<td>{}</td>'.format(entry['ticket'])
    html += '</tr>'

# Pied de page HTML
html += '</tbody>'
html += '</table>'
html += '</body>'
html += '</html>'

# Écriture de la page web
with open('titleKeys.html', 'w', encoding='utf-8') as outfile:  
    outfile.write(html)
    outfile.close()

print('Fini !')