import csv
import os
import datetime


def save_to_csv(data, filename='eth_prices.csv'):
    """
    Save the scraped price data to a CSV file.

    Parameters:
        data (dict): A dictionary containing price information. Example format:
            {
                'Current Price': 2000.5,
                'Pre-market Price': 1990,
                'Post-market Price': 2010,
                'Last Update': '2023-04-01 15:45:30'
            }
        filename (str): The name of the CSV file (default: 'eth_prices.csv')
    """
    # Check if the file already exists
    file_exists = os.path.isfile(filename)

    # Define the headers for the CSV file
    fieldnames = ['Timestamp', 'Current Price', 'Pre-market Price', 'Post-market Price', 'Last Update']

    # Open the CSV file in append mode
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file doesn't exist, write the header row first
        if not file_exists:
            writer.writeheader()

        # Prepare the data row with the current timestamp for when the data was scraped
        row = {
            'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Current Price': data.get('Current Price', 'N/A'),
            'Pre-market Price': data.get('Pre-market Price', 'N/A'),
            'Post-market Price': data.get('Post-market Price', 'N/A'),
            'Last Update': data.get('Last Update', 'N/A')
        }
        writer.writerow(row)
        print(f"Data saved to {filename}")
