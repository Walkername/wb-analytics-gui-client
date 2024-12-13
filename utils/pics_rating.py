import matplotlib.pyplot as plt
from collections import defaultdict

def build_graph(products):
    pics_rating = defaultdict(list)
    
    for product in products:
        # Check if 'priceHistory' exists
        if "pics" and "reviewRating" in product:
            pics = product["pics"]
            reviewRating = product["reviewRating"]
            pics_rating[pics].append(reviewRating)

    pics_list = []
    ratings_list = []
    
    for pic, ratings in pics_rating.items():
        avg_rating = sum(ratings) / len(ratings)
        pics_list.append(pic)
        ratings_list.append(avg_rating)

    # Plot the time series data
    graph = plt.figure(figsize=(10, 6))
    plt.bar(pics_list, ratings_list, color = 'blue', edgecolor='black')
    plt.xlabel('Number of Pictures')
    plt.ylabel('Average Review Rating')
    plt.title('Dependence of product rating on the amount of media content')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    #return graph