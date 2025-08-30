import APIs.bigw_api
from colorama import Fore, Style, init
import json

# Initialize colorama
init(autoreset=True)
outputs = {}
def main():
    big_w_output = APIs.bigw_api.main()
    outputs["Big W"] = big_w_output

    # Function to print stock status with color
    def print_colored_stock(stock_data):
        color_mapping = {
            "outOfStock": Fore.RED,
            "inStock": Fore.GREEN,
            "lowStock": Fore.YELLOW
        }

        # Loop through each product
        for product, stores in stock_data.items():
            print(f"\n{product}:")
            # Loop through each store and print status with color
            for store, status in stores.items():
                if isinstance(status, str):  # Simple status like 'outOfStock'
                    print(f"  {store}: {color_mapping.get(status, Fore.WHITE)}{status}{Style.RESET_ALL}")
                elif isinstance(status, dict):  # Detailed status with 'available' and 'quantity'
                    print(f"  {store}: {color_mapping.get(status['status'], Fore.WHITE)}{status['status']}{Style.RESET_ALL}")

    # Print the stock data with colored status for all stores!
    for website, output in outputs.items():
        print(website)
        print_colored_stock(output)


if __name__ == "__main__":
    _return = main()
    print(_return)