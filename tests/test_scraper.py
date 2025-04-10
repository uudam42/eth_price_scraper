#!/usr/bin/env python3
"""
eth_price_scraper.py

A data scraper that retrieves Ethereum (ETH-USD) price data from Yahoo Finance.

Features:
    - Makes an HTTP GET request to the Yahoo Finance API for ETH-USD price data.
    - Adds a delay between requests to avoid rate-limiting.
    - Parses JSON data to extract current price, pre-market price, post-market price, and the last updated timestamp.
    - Uses logging for information and error messages.
    - Supports command-line arguments for configuring the request interval.

Usage Example:
    python eth_price_scraper.py --interval 5
"""

from data_storage import save_to_csv
import requests  # For making HTTP requests
import datetime  # For handling and formatting timestamps
import time  # For adding delays between requests
import logging  # For logging messages and errors
import argparse  # For parsing command-line arguments

# Configure logging for detailed output
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_price_ethereum(interval=5):
    """
    Retrieves Ethereum (ETH-USD) price data from Yahoo Finance.

    Parameters:
        interval (int): Number of seconds to delay before sending the HTTP request
                        (helps to avoid being blocked due to too frequent requests).

    Returns:
        dict or None: A dictionary containing the current price, pre-market price,
                      post-market price, and the last updated time (formatted as a string).
                      Returns None if an error occurs.
    """
    # Yahoo Finance API endpoint for ETH-USD data
    yh_url = "https://query1.finance.yahoo.com/v8/finance/chart/ETH-USD"

    # HTTP headers to make our request appear as if it were coming from a browser
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Add a delay to prevent hitting rate limits
        time.sleep(interval)

        # Send HTTP GET request to Yahoo Finance API
        response = requests.get(yh_url, headers=headers)
        response.raise_for_status()  # Raise an error for unsuccessful status codes

        # Parse JSON data from the response
        data = response.json()
        meta = data['chart']['result'][0]['meta']

        # Create a dictionary with price information
        price_info = {
            'Current Price': meta['regularMarketPrice'],
            'Pre-market Price': meta.get('preMarketPrice', 'N/A'),
            'Post-market Price': meta.get('postMarketPrice', "N/A"),
            'Last Update': datetime.datetime.fromtimestamp(meta["regularMarketTime"]).strftime("%Y-%m-%d %H:%M:%S")
        }

        logging.info("Successfully retrieved Ethereum price data.")
        return price_info

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request error: {e}")
    except KeyError as e:
        logging.error(f"Error parsing data: {e}")
    except Exception as e:
        logging.error(f"An unknown error occurred: {e}")

    return None


if __name__ == "__main__":
    # Parse command-line arguments for additional configuration
    parser = argparse.ArgumentParser(
        description='Retrieve Ethereum (ETH-USD) price data from Yahoo Finance.')
    parser.add_argument('--interval', type=int, default=5,
                        help='Delay (in seconds) before making the request (default: 5 seconds)')
    args = parser.parse_args()

    # Retrieve Ethereum price data based on the specified interval
    price_data = get_price_ethereum(interval=args.interval)

    # Display the retrieved data, or an error message if data could not be fetched
    if price_data:
        for key, value in price_data.items():
            print(f'{key}: {value}')
    else:
        print('Failed to fetch data.')
