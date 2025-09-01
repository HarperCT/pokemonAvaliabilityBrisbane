import APIs.bigw_api
import APIs.kmart_api
import APIs.morethanmeeples
import logging

from colorama import Fore, Style, init

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # or logging.DEBUG if you want more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize colorama
init(autoreset=True)
def fetch_data():
    outputs = {}
    big_w_output = APIs.bigw_api.main()
    outputs["Big W"] = big_w_output
    kmart_output = APIs.kmart_api.main("4000")
    outputs["Kmart"] = kmart_output
    meeples_output = APIs.morethanmeeples.main()
    outputs["MoreThanMeeples"] = meeples_output
    return outputs

# Function to print stock status with color
def print_colored_stock(stock_data):
    color_mapping = {
        "Low": Fore.RED,
        "outOfStock": Fore.RED,
        "Medium": Fore.YELLOW,
        "lowStock": Fore.YELLOW,
        "High": Fore.GREEN,
        "inStock": Fore.GREEN,
    }
    # Loop through each product
    for product, stores in stock_data.items():
        print(f"\n{product}:")
        if stores is None or product is None:
            logger.warning("howd we get here...")
            continue
        # Loop through each store and print status with color
        for store, status in stores.items():
            if isinstance(status, str):  # Simple status like 'outOfStock'
                print(f"  {store}: {color_mapping.get(status, Fore.WHITE)}{status}{Style.RESET_ALL}")
            elif isinstance(status, dict):  # Detailed status with 'available' and 'quantity'
                print(f"  {store}: {color_mapping.get(status['status'], Fore.WHITE)}{status['status']}{Style.RESET_ALL}")



if __name__ == "__main__":
    data = fetch_data()
    for website, output in data.items():
        print(website)
        if website == "MoreThanMeeples":  # one shot stores...
            APIs.morethanmeeples.print_colored_stock(output)
        else:
            print_colored_stock(output)
