# Create classes here to simplify the routes file!
import requests as r
def getRegions():
    data = r.get('https://pokeapi.co/api/v2/region/')
 

    data = data.json()['results']
    regions = []

    for y in data:
        regions.append(y['name'])   
    return regions



def getCities():
    data = r.get('https://pokeapi.co/api/v2/region/')
    data = data.json()['results']
    regions = []
    regionurls = []
    cities = []
    for y in data: 
        regions.append(y['name'])
        regionurls.append(y['url'])
        rdata = r.get(y['url']).json()
        for i in rdata['locations']:   
            if 'city' in i['name'] or 'town' in i['name'] or 'island' in i['name']:
                cities.append(i['name'].replace('-',' ').title())
    return cities

        


def getCrypto():
    crypto = r.get('https://api.coinlore.net/api/tickers/').json()
    crdict = {}
    crypto
    for i in crypto['data']:
        crdict= {
                'name':i['name'].lower(),
                'symbol':i['symbol'],
                'price_usd':i['price_usd']
                }    

    return crdict   