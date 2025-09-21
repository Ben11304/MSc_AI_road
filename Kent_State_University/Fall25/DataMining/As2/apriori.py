import sys
from collections import defaultdict
import math

def find_frequent_1_itemsets(transactions, min_support_count):
    # Count occurrences of each single item
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    
    # Keep items that meet minimum support
    frequent_items = {frozenset([item]): count for item, count in item_counts.items() if count >= min_support_count}
    return frequent_items

def generate_candidates(prev_frequent, k):
    # Generate k-itemset candidates from (k-1)-itemsets
    candidates = set()
    prev_items = list(prev_frequent.keys())
    for i in range(len(prev_items)):
        for j in range(i + 1, len(prev_items)):
            set1 = prev_items[i]
            set2 = prev_items[j]
            union = set1 | set2
            if len(union) == k:
                candidates.add(union)
    return candidates

def count_supports(candidates, transactions):
    # Count support for each candidate
    supports = defaultdict(int)
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                supports[candidate] += 1
    return supports

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python apriori.py <filename> <min_support_percentage>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        min_support_perc = float(sys.argv[2])
    except ValueError:
        print("Minimum support must be a number (e.g., 15 for 15%)")
        sys.exit(1)

    # Read transactions from file
    try:
        with open(filename, 'r') as f:
            transactions = [set(line.strip().split()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    if not transactions:
        print("No transactions found in the file.")
        return

    # Calculate minimum support count
    total_transactions = len(transactions)
    min_support_count = math.ceil((min_support_perc / 100) * total_transactions)

    # Step 1: Find frequent 1-itemsets
    frequent_itemsets = find_frequent_1_itemsets(transactions, min_support_count)
    all_frequent = frequent_itemsets.copy()

    # Step 2: Generate larger itemsets iteratively
    k = 2
    while frequent_itemsets:
        # Generate candidates for k-itemsets
        candidates = generate_candidates(frequent_itemsets, k)
        if not candidates:
            break

        # Count supports for candidates
        supports = count_supports(candidates, transactions)

        # Keep candidates that meet minimum support
        frequent_itemsets = {itemset: count for itemset, count in supports.items() if count >= min_support_count}
        all_frequent.update(frequent_itemsets)
        k += 1

    # Output frequent itemsets, sorted by size and lexicographically
    for itemset in sorted(all_frequent.keys(), key=lambda x: (len(x), sorted(x))):
        print(' '.join(sorted(itemset)))

if __name__ == "__main__":
    main()