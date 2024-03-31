import requests
import pandas as pd
import re
import sys
from time import sleep


if len(sys.argv) == 1:
    print('Please enter a valid path to an .xlsx file!')
    sys.exit()

path = str(sys.argv[1])

try: 
    df = pd.read_excel(path)
except BaseException as err:
    print(err)
    sys.exit()

name_list = []

for smile in df['Smiles']:
    smile = re.sub('[#]', '%23', smile) # The tripple bond character "#" has to be escaped by %23
    url = f'https://cactus.nci.nih.gov/chemical/structure/{smile}/names'
    #print(f'Looking for Name of {smile}')
    try:
        names = requests.get(url).text
        name = names.partition('\n')[0]
    except BaseException as err:
        name = ''
        print(f'Error: {err}')
    name_list.append(name)
    sleep(1) # No rules for data scraping were found on the page. As required by courtesy, a delay of 1s was used.

#print('Finished!')    

final_df = pd.concat([pd.DataFrame(name_list, columns=(['Name'])), df], axis=1)
final_path = path.partition('.')[-3] + "_named.xlsx"
final_df.to_excel(final_path, index=False)