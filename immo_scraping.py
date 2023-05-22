import requests
from bs4 import BeautifulSoup
from itertools import chain
import csv
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

root_url = 'https://www.immoweb.be'
link_to_find = "https://www.immoweb.be/en/classified/"

def find_links(number):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&propertySubtypes=BUNGALOW,COUNTRY_COTTAGE,APARTMENT_BLOCK,CASTLE,TOWN_HOUSE,VILLA,MANOR_HOUSE,TRIPLEX,PENTHOUSE,FARMHOUSE,EXCEPTIONAL_PROPERTY,MANSION,DUPLEX,LOFT,FLAT_STUDIO&page={number}&orderBy=relevance'
    immo_response = requests.get(url)
    soup = BeautifulSoup(immo_response.text, "html.parser")
    all_links = soup.findAll('a')
    
    links = []
    for link in all_links:
        if link_to_find in link['href']:
            if 'new' not in link['href'].split('/')[-5]:
              links.append(link['href'])
    return links

links = []  
# with ThreadPoolExecutor() as pool:  ((//old way))
#     lists_of_links = list((pool.map(find_links, range(1))))
#     # for list in lists_of_links:
#     #     links.extend(list)
with ThreadPoolExecutor() as pool: 
    links = list(chain.from_iterable(pool.map(find_links, range(10))))

all_data_frames=[]

def get_data_from_ad(link):
    House_details = link.split('/')
    page_response = requests.get(link)
    try:
        tables =pd.read_html(page_response.text)
    except:
        return {}   
    df = pd.concat(tables)
    #----------------------------------------------
    df = df.set_index(0).T
    df['id'] = link.split('/')[-1]
    df = df.set_index('id')
    df = df.loc[:,~df.columns.duplicated()].copy()
    return df

with ThreadPoolExecutor() as pool: 
    properties = pd.concat(pool.map(get_data_from_ad, links))

print(properties)
properties.to_csv('testing.csv')
print('The file has been created successfuly')
# for data_frams in df_list:
#     print(type(data_frams))
    #     total_df = pd.concat(data_frams, axis=1, join='outer')
# print(total_df)
