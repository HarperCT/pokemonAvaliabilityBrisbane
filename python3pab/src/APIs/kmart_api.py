import logging
import requests
import json
import time
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # or logging.DEBUG if you want more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def color_stock_level(level: str) -> str:
    """
    Returns a color-coded string based on stock level:
    - 'High' or 'Medium' => Green
    - everything else => Red
    """
    if level in ["High", "Medium"]:
        return f"{GREEN}{level}{RESET}"
    else:
        return f"{RED}{level}{RESET}"

# Keycodes with associated product names
KEYCODE_PRODUCTS = {
    "43556663": "Elite Trainer Box",
    "43556656": "Sticker Collection",
    "43556649": "Binder Collection",
    "43556632": "Poster Collection",
    "43556670": "Mini Tin"
}

URL = "https://api.kmart.com.au/gateway/graphql"

LOCAL_POST_CODE = "4000"  # Change this

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

def fetch_inventory_for_keycode(keycode: str) -> list:
    """
    Fetch inventory data for a single keycode.
    Returns a list of (locationName, locationId, stockLevel).
    """
    payload = {
        "operationName": "getFindInStore",
        "variables": {
            "input": {
                "postcode": LOCAL_POST_CODE,
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

def main():
    polling_interval = 300  # 5 minutes = 300 seconds
    logger.info("Starting to poll stock levels every 5 minutes...")

    while True:
        # 1. Fetch data for ALL keycodes first
        all_results = {}
        for keycode, product_name in KEYCODE_PRODUCTS.items():
            stores = fetch_inventory_for_keycode(keycode)
            all_results[keycode] = stores

        # 2. After all requests, print them in a table for each keycode
        for keycode, product_name in KEYCODE_PRODUCTS.items():
            # Prepare table data: a list of rows
            # We'll color the stock level
            table_data = []
            for (loc_name, loc_id, stock_level) in all_results[keycode]:
                colored_stock = color_stock_level(stock_level)
                table_data.append([loc_name, loc_id, colored_stock])

            # Generate a table string using tabulate
            table_str = tabulate(
                table_data,
                headers=["Store", "Location ID", "Stock Level"],
                tablefmt="psql"
            )

            # Print a header line with keycode and product name
            logger.info("Keycode: %s - %s", keycode, product_name)

            # Each line of the table gets logged so timestamps/levels appear
            for line in table_str.split("\n"):
                logger.info(line)

        logger.info("Finished this polling cycle. Sleeping for 5 minutes...\n")
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()