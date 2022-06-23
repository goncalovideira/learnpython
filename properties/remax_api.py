from dataclasses import replace
import requests
import math
import pandas as pd
from datetime import datetime

print(str(datetime.utcnow()).replace('.','_').replace(':','-'))

url = 'https://www.remax.pt/Api/Listing/MultiMatchSearch'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }

payload = {
    "filters":[
        {"field":"BusinessTypeID","value":"1","type":0},
        {"field":"ListingTypeID","shouldValues":["11"],"type":2},
        {"field":"Region2ID","value":"537","type":0}],
        "sort":{"fieldToSort":"ContractDate","order":1}}

size=20 # max is 10000

query_payload = {
    'page':0,
    'searchValue':'',
    'size':size
    }

jsonData = requests.post(url, params=query_payload, json=payload).json()

total_pages = math.ceil(jsonData['total']/size)

element_list = []
for page in range(0,total_pages+1):
    if page != 0:
        query_payload.update({'page':page})
        jsonData = requests.post(url, params=query_payload,json=payload, headers=headers).json()
        
    if len(jsonData['results']) == 0:
           break
    element_list += jsonData['results']
    print('Collected: Page %s: %s listings' %(page+1, len(jsonData['results'])))
    
listing_df = pd.DataFrame(element_list)

rows = []
listing_ids = list(listing_df['listingTitle'])
for idx, listing_id in enumerate(listing_ids):
    listing_url = 'https://s.maxwork.pt/site/static/9/listings/details_V2/%s.html' %listing_id
    response = requests.get(listing_url, headers=headers) 

    with open(f"C:/Users/gonca/OneDrive - BYZAPP LABS/DeveloperPlan/learnpython/properties/data/{listing_id}.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # check for the existence of features
    try: 
        temp_features = pd.read_html(response.text)[1]

        # process features
        alpha = temp_features.iloc[:,[0]]
        beta = temp_features.iloc[:,[1]]
        beta.columns = alpha.columns
        features_raw = pd.concat([alpha,beta], axis=0)
        features_raw.dropna(axis=0,inplace=True)
        features = features_raw[0].to_list()
        features_str = ';'.join(features)
    
    except:
        features = []
        features_str = ''

    # check for the existence of details
    temp_details = pd.read_html(response.text)[0]

    # process details
    alpha = temp_details.iloc[:,[0,1]]
    beta = temp_details.iloc[:,[2,3]]
    beta.columns = alpha.columns
    temp_df = pd.DataFrame([['Outros', features_str]])
    temp_df.columns = alpha.columns
    details = pd.concat([alpha,beta,temp_df])

    print(details)

    details['listingTitle'] = listing_id
    details = details.pivot(index='listingTitle',columns=0,values=1).reset_index(drop=False)
    rows += details.to_dict(orient='records')
    
    print('%s of %s' %(idx+1,len(listing_ids)))
    print('\n')
    
listing_desc_df = pd.DataFrame(rows)

df = listing_df.merge(listing_desc_df, how='left', on=['listingTitle'])
print(df.columns)
df.drop(columns=['autocompleteListingTitle', 'coordinates', 'listingPriceText',
       'listingTypeID', 'isSpecial', 'listingPictures', 'region2ID', 'region3ID'], inplace=True)
df.dropna(axis=1,how='all',inplace=True)
df.rename(
    columns={
        'listingTitle': 'listingID',
        'isSold': 'sold',
        'longitude': 'longitude',
        'latitude': 'latitude',
        'listingPrice': 'Price',
        'regionName1': 'district',
        'regionName2': 'county',
        'regionName3': 'parish',
        'listingMetatagTitle': 'Title',
        'listingMetatagDescription': 'Description',
        'Ano de construção': 'Ano',
        'Elevador': 'lift',
        'Estacionamento': 'parking',
        'Outros':'others',
        'Piso': 'floor',
        'Quartos': 'type',
        'WCs': 'toilets',
        'Área Bruta Privativa m2': 'private_area',
        'Área Bruta m2': 'area_gross',
        'Área Total do Lote m2': 'total_area',
        'Área Útil m2': 'net_area',
        'Carregamento de Carros Elétricos': 'EVcharging'
    },
    inplace=True
)

df.to_csv('listings ' + str(datetime.utcnow()).replace('.','_').replace(':','-') + '.csv')