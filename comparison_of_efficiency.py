from BTrees.OOBTree import OOBTree
from time import time
import csv


def load_data_from_csv(filename):
    items = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_id = int(row["ID"])
            items[item_id] = {
                "name": row["Name"],
                "category": row["Category"],
                "price": float(row["Price"]),
            }
    return items


def add_item_to_tree(tree, items):
    start = time()
    for item_id, item in items.items():
        tree[item_id] = item
    end = time()
    time_tree = end - start
    return time_tree


def add_item_to_dict(my_dict, items):
    start = time()
    my_dict.update(items)
    end = time()
    time_dict = end - start
    return time_dict


def range_query_tree(tree, min_price, max_price):
    start = time()
    for _, item in tree.items(min_price, max_price):
        if item["price"] >= min_price and item["price"] <= max_price:
            item
    end = time()
    time_tree = end - start
    return time_tree


def range_query_dict(my_dict, min_price, max_price):
    start = time()
    for item in my_dict.values():
        if item["price"] >= min_price and item["price"] <= max_price:
            item
    end = time()
    time_dict = end - start
    return time_dict


if __name__ == "__main__":
    filename = "generated_items_data.csv"
    items = load_data_from_csv(filename)

    tree = OOBTree()
    my_dict = {}

    add_item_to_tree(tree, items)
    add_item_to_dict(my_dict, items)

    min_price = 10.0
    max_price = 250.0

    total_time_tree = 0
    total_time_dict = 0

    for _ in range(1000):
        total_time_tree += range_query_tree(tree, min_price, max_price)
        total_time_dict += range_query_dict(my_dict, min_price, max_price)

    print(f"Total range_query time for OOBTree: {total_time_tree:.6f} seconds")
    print(f"Total range_query time for Dict: {total_time_dict:.6f} seconds")
