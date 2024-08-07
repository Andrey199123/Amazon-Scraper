import json
import sys
import glob
import os

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_titles(data):
    return [product['title'] for product in data]

def get_price(data):
    return [product['price'] for product in data]

def map_products_by_title(data):
    return {product['title']: product for product in data}

def find_matching_product(title, titles, products):
    for other_title in titles:
        if title in other_title:
            return products.get(other_title)
    return None

def correct_prices(file1, file2):
    data1 = load_json(file1)
    data2 = load_json(file2)

    products1 = map_products_by_title(data1)
    products2 = map_products_by_title(data2)

    titles2 = get_titles(data2)

    for title, product1 in products1.items():
        product2 = find_matching_product(title, titles2, products2)

        if product2:
            # Correct price in file1 using file2
            if product1['price'] is None and product2['price'] is not None:
                product1['price'] = product2['price']
            # Correct price in file2 using file1
            if product2['price'] is None and product1['price'] is not None:
                product2['price'] = product1['price']

    titles1 = get_titles(data1)
    
    for title, product2 in products2.items():
        product1 = find_matching_product(title, titles1, products1)
        
        if product1:
            # Correct price in file2 using file1
            if product2['price'] is None and product1['price'] is not None:
                product2['price'] = product1['price']
            # Correct price in file1 using file2
            if product1['price'] is None and product2['price'] is not None:
                product1['price'] = product2['price']

    # Save the corrected data back to the files
    save_json(file1, list(products1.values()))
    save_json(file2, list(products2.values()))

def edit_title(file):
    data = load_json(file)
    products = map_products_by_title(data)
    for title, product in products.items():
        product['title'] = product['title'].replace("…", '')
    return data

def main(file1, file2):
    data1 = edit_title(file1)
    data2 = edit_title(file2)

    save_json(file1, data1)
    save_json(file2, data2)

    correct_prices(file1, file2)
    correct_prices(file2, file1)
    print(f"Prices corrected in {file1} and {file2}")

if __name__ == "__main__":
    # Find all JSON files starting with "products"
    product_files = glob.glob("products*.json")

    if len(product_files) < 2:
        print("Not enough product files to compare. Ensure there are at least two files starting with 'products'.")
        sys.exit(1)

    # Process each pair of files
    for i in range(len(product_files)):
        for j in range(i + 1, len(product_files)):
            file1 = product_files[i]
            file2 = product_files[j]
            print(f"Processing {file1} and {file2}")
            main(file1, file2)