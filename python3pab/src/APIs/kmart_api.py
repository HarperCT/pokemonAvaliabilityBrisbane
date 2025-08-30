import logging
import requests
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # or logging.DEBUG if you want more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Keycodes with associated product names
KEYCODE_PRODUCTS = {
    "Pokemon Trading Card Game: Scarlet & Violet Prismatic Evolutions Elite Trainer Box": "43556663",
    "Pokemon Trading Card Game: Scarlet and Violet 151 Zapdos Ex Collection": "43350230",
    "Pokemon Trading Card Game: Scarlet & Violet Prismatic Evolutions Booster Bundle": "43556700",
    "Pokemon Trading Card Game: Scarlet and Violet White Flare Booster Bundle": "43615735",
    "Pokemon Trading Card Game: Scarlet and Violet Black Bolt Booster Bundle": "43615742",
    "Pokemon Trading Card Game Holiday Calendar": "43647248",
    "Pokemon Trading Card Game: Scarlet & Violet Surging Sparks Booster Bundle": "43519750",
    "Pokemon Trading Card Game: Scarlet and Violet Black Bolt and White Flare Victini Illustration Collection": "43615728",
    "Pokemon Trading Card Game: Scarlet and Violet 151 Booster Bundle": "43350070",
    "Pokemon Trading Card Game: Scarlet & Violet Destined Rivals Elite Trainer Box": "43601219",
    "Pokemon Trading Card Game: Unova Mini Tin - Assorted": "43615667",
    "Pokemon Trading Card Game: Scarlet & Violet 151 Alakazam Ex Collection": "43350223",
    "Pokemon Trading Card Game: Scarlet and Violet White Flare Elite Trainer Box": "43615643",
    "Pokemon Trading Card Game: Slashing Legends Tin - Assorted": "43612154",
    "Pokemon Trading Card Game: Scarlet & Violet Destined Rivals Blister Pack - Assorted": "43601165",
    "Pokemon Trading Card Game: Charizard ex Super-Premium Collection": "43510948",
    "Pokemon Trading Card Game: Scarlet & Violet Prismatic Evolutions Surprise Box - Assorted": "43556687",
    "Pokemon Trading Card Game: Scarlet & Violet Surging Sparks Elite Trainer Box": "43519804",
}

URL = "https://api.kmart.com.au/gateway/graphql"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-AU,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://www.kmart.com.au/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def fetch_inventory_for_keycode(keycode: str, postcode: str) -> list:
    """
    Fetch inventory data for a single keycode.
    Returns a list of (locationName, locationId, stockLevel).
    """
    payload = {
        "operationName": "getFindInStore",
        "variables": {
            "input": {
                "postcode": postcode,
                "country": "AU",
                "keycodes": [keycode]
            }
        },
        "query": """query getFindInStore($input: FindInStoreQueryInput!) {
          findInStoreQuery(input: $input) {
            keycode
            inventory {
              locationName
              locationId
              stockLevel
              phoneNumber
              __typename
            }
            __typename
          }
        }"""
    }

    logger.debug("Fetching inventory for keycode %s with payload:\n%s",
                 keycode, json.dumps(payload, indent=2))

    response = requests.post(URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()

    # Navigate into the structure
    find_in_store = data.get("data", {}).get("findInStoreQuery", [])
    if not find_in_store:
        logger.warning("No data returned for keycode %s", keycode)
        return []

    # Usually find_in_store[0] corresponds to this keycode
    inventory_entries = find_in_store[0].get("inventory", [])

    results = []
    for store in inventory_entries:
        loc_name = store["locationName"]
        loc_id = store["locationId"]
        stock_level = store["stockLevel"]
        results.append((loc_name, loc_id, stock_level))

    return results

def main(postcode: str):

    all_results = {}
    nice_json = {}
    for product_name, keycode in KEYCODE_PRODUCTS.items():
        stores = fetch_inventory_for_keycode(keycode, postcode)
        all_results[product_name] = stores
        nice_json[product_name] = {}
        for (loc_name, _loc_id, stock_level) in all_results[product_name]:
            nice_json[product_name][loc_name] = stock_level
    return nice_json

if __name__ == "__main__":
    x = main("4000")
    logger.info(x)
    y = main("4207")
    logger.info(y)
