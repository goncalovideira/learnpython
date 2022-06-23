import pandas as pd



df = pd.read_csv('listings 2022-06-20 17-36-16_461245.csv')

df.drop(columns=['Unnamed: 0', 'autocompleteListingTitle', 'coordinates', 'listingPriceText',
       'listingTypeID', 'isSpecial', 'listingPictures', 'region2ID', 'region3ID','Unnamed: 30'], inplace=True)

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
print(df.columns)
print('\n')

