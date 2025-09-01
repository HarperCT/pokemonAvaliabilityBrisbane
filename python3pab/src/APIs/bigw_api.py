import urllib3
import json
import logging

stock_api = "https://api.bigw.com.au/api/availability/v0/product/"
base_bigw_url = "https://www.bigw.com.au/"  # For cookies
logger = logging.getLogger(__name__)

PRODUCTS = {
    "Pokemon TCG: Charizard ex Super-Premium Collection": 942021,
    "Pokemon TCG Battle Academy": 906112,
    "Pokemon TCG: Paradox Destinies Tin** - Assorted*": 920548,
    "Pokemon TCG: Best Of Pokeball Tin - Assorted*": 6029858,
    "Pokemon TCG: Scarlet & Violet Surging Sparks Booster Display - Assorted*": 52613,
    "Pokemon TCG: Scarlet & Violet Twilight Masquerade Booster Bundle": 906105,
    "Pokémon TCG: Scarlet & Violet - Twilight Masquerade Booster Display (36 Booster Packs)": 906107,
    "Pokémon TCG: Mew VMAX League Battle Deck": 250448,
    "Pokémon TCG: Holiday Calendar": 6038508,
    # "Pokémon TCG: Mega Evolution Blister - Assorted*": 6038711  #TODO make the pre-order things work...
}

STORE_IDS = {
    "Macarthur": "0278",
    "Brookside": "0237",
    "Chermside": "0248",
    "Carindale": "0255",
    "Upper Mt Gravatt": "0272",
    "Mt Ommaney": "0270",
    "Taigum": "0277",
    "Underwood": "0252",
    "Strathpine": "0262",
    "Capalaba": "0266",
    "Redbank": "0238",
    "Browns Plains": "0267",
    "North Lakes": "0246",
    "Loganholme": "0274",
    "Springfield": "0282",
    "Booval": "0265",
    "Beenleigh": "0275",
    "Morayfield": "0285",
    "Runaway Bay": "0269",
    "Pacific Fair": "0261",
}

def main():
    logger.info("Starting BigW API")
    nice_json = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-BIGW-ZoneId': 'BRISBANE-CITY-4000'
    }

    http = urllib3.PoolManager(headers=headers)
    response = http.request('GET', base_bigw_url, timeout=20.0)
    set_cookie_header = response.headers.get('Set-Cookie')
    headers["set-cookie"] = set_cookie_header
    all_stores_url = "?"
    for storeid in STORE_IDS.values():
        all_stores_url += f"storeId={storeid}&"
    
    # pop the last & from stores_url
    all_stores_url = all_stores_url[:-1]

    for key, value in PRODUCTS.items():
        final_stock_api = stock_api + str(value) + all_stores_url
        nice_json[key] = {}
        stock_response = http.request(
            'GET',
            final_stock_api,
            headers=headers
        )

        response_json = json.loads(stock_response.data.decode())

        instore = response_json["products"][f"{value}"]["instore"]
        for key2, value2 in instore.items():
            if key2 in STORE_IDS.values():
                # Find the key corresponding to the value
                store_name = [key for key, value in STORE_IDS.items() if value == key2][0]
                # Change key2 to the corresponding store name
                key2 = store_name
            if value2["status"] == "inStock":
                nice_json[key][key2] = value2
            else:
                nice_json[key][key2] = value2["status"]
    logger.info("Finished BigW API")

    return nice_json

if __name__ == "__main__":
    _return = main()
    print(_return)