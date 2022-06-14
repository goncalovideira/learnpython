from dataclasses import replace
import requests
import math
import pandas as pd
from datetime import datetime

print(str(datetime.utcnow()).replace('.','_').replace(':','-'))

url = 'https://www.remax.pt/Api/Listing/MultiMatchSearch'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
payload = {"filters":
           [{'field':'BusinessTypeID','value':'1','type':0},
            {'field':'ListingClassID','value':'1','type':0},
            {'field':'Region2ID','value':'400','type': 0}],
           'sort':{'fieldToSort':'ContractDate','order':1}}
size=200 # max is 10000
query_payload = {
'page':0,
'searchValue':'',
'size':size}

    
jsonData = requests.post(url, params=query_payload,json=payload).json()
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
    temp_details = pd.read_html(response.text)[0]

    alpha = temp_details.iloc[:,[0,1]]
    beta = temp_details.iloc[:,[2,3]]
    beta.columns = alpha.columns
    details = pd.concat([alpha,beta])
    details['listingTitle'] = listing_id
    details = details.pivot(index='listingTitle',columns=0,values=1).reset_index(drop=False)
    rows += details.to_dict(orient='records')
    
    print('%s of %s' %(idx+1,len(listing_ids)))
    
listing_desc_df = pd.DataFrame(rows)

df = listing_df.merge(listing_desc_df, how='left', on=['listingTitle'])

df.to_csv('listings ' + str(datetime.utcnow()).replace('.','_').replace(':','-') + '.csv')