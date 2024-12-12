
import pymongo
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
import db_service

# Function to get the start of the 7-day interval for a given timestamp
def get_week_start(date_obj):
    # Calculate the start of the week (7-day interval starts on the same weekday as the given date)
    return date_obj - timedelta(days=date_obj.weekday())

def build_graph(entities):
    url = "mongodb://localhost:27017/"
    db = "wb-products"
    col_name = "products"
    #entities = ["Куртки", "Дутики", "Свитеры", "Водолазки", "Костюмы", "Толстовки", "Джинсы"]
    products = db_service.get_by_entities(url, db, col_name, entities)
    
    # Dictionary to hold prices for each timestamp (timestamp: [price1, price2, ...])
    timestamp_prices = defaultdict(list)

    # Iterate over all products
    for product in products:
        # Check if 'priceHistory' exists
        if "priceHistory" in product:
            for record in product["priceHistory"]:
                timestamp = record["time"]
                timestamp = int(timestamp)
                if (timestamp < 1722500000):
                    continue
                if (timestamp > 1731013200):
                    continue
                price = record["price"] / 100  # Convert from kop to rubles
                
                # Add the price to the dictionary keyed by timestamp
                timestamp_prices[timestamp].append(price)

    # Prepare lists for plotting
    timestamps = []
    average_prices = []

    # New dictionary to hold combined prices by date
    comb_dict = defaultdict(list)

    for timestamp, prices in timestamp_prices.items():
        # Extract the date part of the timestamp (e.g., '2024-12-06')
        timestamp_int = int(timestamp)
        #date = datetime.utcfromtimestamp(timestamp_int).strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
        date = datetime.utcfromtimestamp(timestamp_int)
        # Get the start of the 7-day interval
        week_start = get_week_start(date)
        # Use the week start as the key, formatted as a string
        week_key = week_start.strftime('%Y-%m-%d')
        
        # Add prices to the list for that specific day
        comb_dict[week_key].extend(prices)

    # Calculate average prices for each timestamp
    for date, prices in sorted(comb_dict.items()):
        avg_price = sum(prices) / len(prices)  # Average of all prices at this timestamp
        print(f"{date}: {len(prices)}")
        timestamps.append(date)
        average_prices.append(avg_price)
        
        print(f"")

    print(f"size timestamps: {len(timestamps)}")

    new_dates = []

    for date in timestamps:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        
        # Format the date as "day month" (e.g., "28 August")
        new_dates.append(date_obj.strftime('%d %B'))

    # Plot the time series data
    graph = plt.figure(figsize=(10, 6))
    plt.plot(new_dates, average_prices, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Price (RUB)')
    plt.title('Average Price History Across All Products')
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()
    
    #return graph

#build_graph()