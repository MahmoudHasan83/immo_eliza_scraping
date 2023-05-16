import requests
from bs4 import BeautifulSoup
from itertools import chain
import csv
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

root_url = 'https://www.immoweb.be'
link_to_find = "https://www.immoweb.be/en/classified/"

def find_links(number):
    url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&propertySubtypes=BUNGALOW,CASTLE,COUNTRY_COTTAGE,APARTMENT_BLOCK,TOWN_HOUSE,VILLA,MANOR_HOUSE,GROUND_FLOOR,TRIPLEX,PENTHOUSE,KOT,CHALET,FARMHOUSE,EXCEPTIONAL_PROPERTY,MANSION,DUPLEX,FLAT_STUDIO,LOFT&isNewlyBuilt=false&page={number}&orderBy=relevance'
    #url = f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&propertySubtypes=BUNGALOW,COUNTRY_COTTAGE,APARTMENT_BLOCK,CASTLE,TOWN_HOUSE,VILLA,MANOR_HOUSE,TRIPLEX,PENTHOUSE,FARMHOUSE,EXCEPTIONAL_PROPERTY,MANSION,DUPLEX,LOFT,FLAT_STUDIO&page={number}&orderBy=relevance'
    immo_response = requests.get(url)
    soup = BeautifulSoup(immo_response.text, "html.parser")
    all_links = soup.findAll('a')
    
    links = []
    for link in all_links:
        if link_to_find in link['href']:
            links.append(link['href'])

    return links

links = []  
# with ThreadPoolExecutor() as pool:  ((//old way))
#     lists_of_links = list((pool.map(find_links, range(1))))
#     # for list in lists_of_links:
#     #     links.extend(list)
with ThreadPoolExecutor() as pool: 
    links = list(chain.from_iterable(pool.map(find_links, range(300))))



def get_data_from_ad(link):
    
    page_response = requests.get(link)
    try:
        tables =pd.read_html(page_response.text)
    except:
        return {}
    data_dict = {}

    for tab in range(len(tables) - 1):
        for i in range(1):
            for j in range(len(tables[tab][i])):
                index = tables[tab][i][j]
                data_dict[index] = tables[tab][i+1][j]

    
    House_details = link.split('/')

    if 'Neighbourhood or locality' not in data_dict:
        locality = None
    else:
        locality = data_dict['Neighbourhood or locality']
    
    
    city_name = House_details[7]
    
    T_property = House_details[5]
    
    if 'Price' not in data_dict:
        Price = None
    else:
        Price = data_dict['Price'].split()[1] + " " + data_dict['Price'].split()[3]
    
    if 'Bedrooms' not in data_dict:
        Bedrooms = None
    else:
        Bedrooms = data_dict['Bedrooms']
    
    if 'Living area' not in data_dict:
        Living_area = None
    else:
        Living_area = data_dict['Living area'].split()[0] + " " + data_dict['Living area'].split()[1]
    
    if 'Kitchen type' not in data_dict:
        kitchen_type = None
    else:
        kitchen_type = data_dict['Kitchen type']
    
    if 'Furnished' not in data_dict:
        Furnished = None
    else:
        Furnished = data_dict['Furnished']
    

    if 'Garden surface' not in data_dict:
        Garden = 0
    else:
        Garden = data_dict['Garden surface']
    

    if 'Terrace surface' not in data_dict:
        Terrace = 0
    else:
        Terrace = data_dict['Terrace surface']
    

    if 'Surface of the plot' not in data_dict:
        plot_surface = None
    else:
        plot_surface = data_dict['Surface of the plot']
    
    if 'Swimming pool' not in data_dict:
        Swimming_pool = None
    else:
        Swimming_pool = data_dict['Swimming pool']
    
    if 'Building condition' not in data_dict:
        Building_condition = None
    else:
        Building_condition = data_dict['Building condition']
    
    if 'Number of frontages' not in data_dict:
        Nr_of_facade = None
    else:
        Nr_of_facade = data_dict['Number of frontages']
    
    
    
    return [{'City':city_name,'locality':locality,'Type of property':T_property, 'Price':Price,'Bed rooms':Bedrooms,'Living Area':Living_area, 'Fully equipped kitchen':kitchen_type,'Furnished':Furnished,'Terrace':Terrace,'Garden':Garden,' Surface Area of the plot':plot_surface,'Number of facade':Nr_of_facade,'Swimming pool':Swimming_pool,'State of the building':Building_condition}]
   
with ThreadPoolExecutor() as pool: 
    info_dict = list(chain.from_iterable(pool.map(get_data_from_ad, links)))

keys = ['City', 'locality', 'Type of property', 'Price', 'Bed rooms', 'Living Area', 'Fully equipped kitchen', 'Furnished', 'Terrace', 'Garden', ' Surface Area of the plot', 'Number of facade', 'Swimming pool', 'State of the building']

with open('houses.csv','w') as data:
        dict_writer = csv.DictWriter(data, keys)
        dict_writer.writeheader()
        dict_writer.writerows(info_dict)
        print(' File has been successfuly created')

