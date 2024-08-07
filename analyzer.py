import json
import sys
import re

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_titles(data):
    return [product['title'] for product in data if isinstance(product, dict)]

def find_matching_product(title, titles):
    for other_title in titles:
        if title in other_title or other_title in title:
            return True
    return False

def find_unique_products(file1, file2):
    data1 = load_json(file1)
    data2 = load_json(file2)

    titles1 = get_titles(data1)
    titles2 = get_titles(data2)

    unique_to_file1 = [title for title in titles1 if not find_matching_product(title, titles2)]
    unique_to_file2 = [title for title in titles2 if not find_matching_product(title, titles1)]

    unique_products_file1 = [product for product in data1 if product['title'] in unique_to_file1]
    unique_products_file2 = [product for product in data2 if product['title'] in unique_to_file2]

    return unique_products_file1, unique_products_file2

def compute_averages(data):
    total_price = 0
    total_rating = 0
    total_reviews = 0
    count_price = 0
    count_rating = 0
    count_reviews = 0

    for product in data:
        # Handle price if it exists and is not None
        if product['price']:
            # Remove the currency symbol and convert to float
            price = float(product['price'].replace('€', '').replace(',', '.'))
            total_price += price
            count_price += 1
        
        # Handle rating if it exists and is not None
        if product['rating']:
            total_rating += product['rating']
            count_rating += 1
        
        # Handle reviewsCount if it exists and is not None
        if product['reviewsCount']:
            total_reviews += product['reviewsCount']
            count_reviews += 1
    
    # Compute averages
    average_price = total_price / count_price if count_price else None
    average_rating = total_rating / count_rating if count_rating else None
    average_reviews = total_reviews / count_reviews if count_reviews else None

    return average_price, average_rating, average_reviews

def find_and_compare_products(file1, file2):
    data1 = load_json(file1)
    data2 = load_json(file2)

    titles1 = get_titles(data1)
    titles2 = get_titles(data2)

    matched_products = []

    for product1 in data1:
        title1 = product1['title']
        for product2 in data2:
            title2 = product2['title']
            if title1 in title2 or title2 in title1:
                # Compare price, rating, and number of ratings
                price1 = product1.get('price')
                price2 = product2.get('price')
                rating1 = product1.get('rating')
                rating2 = product2.get('rating')
                num_ratings1 = product1.get('reviewsCount')
                num_ratings2 = product2.get('reviewsCount')
                print(f"{title1}")
                if price1 is not None and price2 is not None and price1 != price2:
                    diff = round(float(price2[:-1]) - float(price1[:-1]), 2)
                    if diff > 0:
                        diff = "%+0.2f" % diff
                    print(f"Price change: {price1} -> {price2} ({diff})")
                
                if rating1 is not None and rating2 is not None and rating1 != rating2:
                    diff = round(float(rating2) - float(rating1), 1)
                    if diff > 0:
                        diff = "%+0.1f" % diff
                    print(f"Rating change: {rating1} -> {rating2} ({diff})")
                
                if num_ratings1 is not None and num_ratings2 is not None and num_ratings1 != num_ratings2:
                    diff = int(num_ratings2) - int(num_ratings1)
                    if diff > 0:
                        diff = "+" + str(diff)
                    print(f"Number of ratings change: {num_ratings1} -> {num_ratings2} ({diff})")
                print('\n')
                matched_products.append((title1, product1, product2))

    return matched_products

def print_averages(file_path, averages):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path)
    date_part = match.group(1)
    print(f"Averages for {date_part}:")
    print(f"Average price: {averages[0]:.2f}€" if averages[0] else "Average price: N/A")
    print(f"Average rating: {averages[1]:.2f}" if averages[1] else "Average rating: N/A")
    print(f"Average reviews: {averages[2]:.2f}" if averages[2] else "Average reviews: N/A")
    print()

def main(file1, file2):
    # Load data from file1
    with open(file1, 'r') as f:
        data1 = json.load(f)

    # Load data from file2
    with open(file2, 'r') as f:
        data2 = json.load(f)

    # Compute averages for both files
    averages1 = compute_averages(data1)
    averages2 = compute_averages(data2)

    # Print averages
    print_averages(file1, averages1)
    print_averages(file2, averages2)

    unique_products_file1, unique_products_file2 = find_unique_products(file1, file2)

    print("\nRemoved Products (" + str(len(unique_products_file1)) + "):\n")
    for product in unique_products_file1:
        print(product['title'])
    print('\n')
    print("\nAdded Products (" + str(len(unique_products_file2)) + "):\n")
    for product in unique_products_file2:
        print(product['title'])
    print('\n')
    find_and_compare_products(file1, file2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyzer.py <file1.json> <file2.json>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    main(file1, file2)