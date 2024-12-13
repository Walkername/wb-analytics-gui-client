import matplotlib.pyplot as plt
from collections import defaultdict

def build_graph(products):
    product_sizes = defaultdict(list)
    
    for product in products:
        # Check if 'priceHistory' exists
        if "sizes" in product:
            min_rank = 999999
            size_name = ""
            for size in product["sizes"]:
                if "rank" and "name" in size:
                    rank = size["rank"]
                    if rank < min_rank:
                        min_rank = rank
                        if (size["name"].isdigit()):
                            size_name = size["name"]
                            
            if (size_name != ""): 
                size_name = int(size_name)
                if (size_name > 30 and size_name < 60):
                    product_sizes[int(size_name)].append(1)

    sizes = []
    quantities = []
    
    for size, numbers in sorted(product_sizes.items()):
        quantities.append(len(numbers))
        sizes.append(size)
        
    print(f"len sizes: {len(sizes)}")

    # Plot the time series data
    graph = plt.figure(figsize=(10, 6))
    bars = plt.bar(sizes, quantities, color = 'blue', edgecolor='black')
    
    # Add text inside the bars
    for bar, label in zip(bars, sizes):
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # Horizontal position
            bar.get_height() + 0.5,              # Vertical position
            label,                             # Text to display
            ha='center',                       # Horizontal alignment
            va='bottom',                       # Vertical alignment
            fontsize=10                        # Font size
        )
    
    plt.xlabel('Number of Pictures')
    plt.ylabel('Average Review Rating')
    plt.title('Dependence of product rating on the amount of media content')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
