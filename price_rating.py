import pymongo
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
import db_service

def build_graph(entities):
    url = "mongodb://localhost:27017/"
    db = "wb-products"
    col_name = "products"
    products = db_service.get_by_entities(url, db, col_name, entities)
    
    #timestamp_prices[timestamp].append(price)
    
    price_rating = defaultdict(list)
    
    for product in products:
        # Check if 'priceHistory' exists
        if "sizes" and "reviewRating" in product:
            if product["reviewRating"] == 0:
                continue
            
            sizes = product["sizes"]
            
            for size in sizes:
                discount_price = size["discountPrice"] / 100
                basic_price = size["basicPrice"] / 100
                difference = basic_price - discount_price
                ratio = (difference / basic_price) * 100
                reviewRating = round(product["reviewRating"])
                        
                price_rating[reviewRating].append(ratio)
    
    difference_list = []
    ratings_list = []
    
    for rating, differences in price_rating.items():
        print(f"{rating}: {len(differences)}")
        avg_price = sum(differences) / len(differences)
        difference_list.append(avg_price)
        ratings_list.append(rating)

    # Plot the time series data
    graph = plt.figure(figsize=(10, 6))
    plt.plot(ratings_list, difference_list, marker='o', linestyle='-', color='b')
    #plt.bar(ratings_list, price_list, color = 'blue', edgecolor='black')
    plt.xlabel('Review Ratings')
    plt.ylabel('Average Price (RUB)')
    plt.title('Dependence of product rating on the price')
    plt.grid(True)
    plt.tight_layout()
    
    plt.show()
    
    #return graph

#build_graph()