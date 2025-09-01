import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger(__name__)

url = "https://morethanmeeples.com.au/buy-pokemon-cards-online/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://morethanmeeples.com.au/",
}
def main():
    logger.info("Starting Meeples API")
    response = requests.get(url, headers=headers)

    html = response.text

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Build product availability dict
    product_availability = {}

    products = soup.find_all("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")

    for product in products:
        href = product.get("href", "")
        
        # Extract product slug from URL
        if "/product/" in href:
            slug = href.split("/product/")[-1].strip("/")
        else:
            continue  # skip anything unexpected

        # Determine stock status
        out_of_stock = product.find("span", class_="outofstock_label")
        stock_status = "Out of Stock" if out_of_stock else "In Stock"

        product_availability[slug] = stock_status

    # Output as pretty JSON
    logger.info("Finished Meeples API")
    return product_availability

def print_colored_stock(stock_data):
    color_mapping = {
        "Out of Stock": Fore.RED,
        "In Stock": Fore.GREEN,
    }

    for product, status in stock_data.items():
        color = color_mapping.get(status, Fore.WHITE)
        print(f"  {product}: {color}{status}{Style.RESET_ALL}")

if __name__ == "__main__":
    x = main()
    print_colored_stock(x)