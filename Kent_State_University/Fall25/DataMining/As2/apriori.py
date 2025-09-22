import sys
from collections import defaultdict
import math

def find_frequent_1_itemsets(transactions, min_support_count):
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item]+=1
    frequent_items ={frozenset([item]):count for item,count in item_counts.items() if count>=min_support_count}
    return frequent_items

def generate_candidates(prev_frequent, k):
    candidates= set()
    prev_items= list(prev_frequent.keys())
    for i in range(len(prev_items)):
        for j in range(i+1, len(prev_items)):
            set1= prev_items[i]
            set2 =prev_items[j]
            union =set1|set2
            if len(union)== k:
                candidates.add(union)
    return candidates

def count_supports(candidates,transactions):
    supports =defaultdict(int)
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                supports[candidate] +=1
    return supports

def main():
    filename = sys.argv[1]
    try:
        min_support_perc = float(sys.argv[2])
    except ValueError:
        print("lack of minimum fequent percentage")
        sys.exit(1)
    try:
        with open(filename, 'r') as f:
            transactions = [set(line.strip().split()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not available")
        sys.exit(1)

    if not transactions:
        print("No transactions")
        return

    total_transactions = len(transactions)
    min_support_count =math.ceil((min_support_perc / 100) * total_transactions)

    frequent_itemsets = find_frequent_1_itemsets(transactions, min_support_count)
    all_frequent = frequent_itemsets.copy()

    k = 2
    while frequent_itemsets:
        candidates = generate_candidates(frequent_itemsets, k)
        if not candidates:
            break
        supports =count_supports(candidates, transactions)
        frequent_itemsets = {itemset: count for itemset, count in supports.items() if count >= min_support_count}
        all_frequent.update(frequent_itemsets)
        k +=1
        
    for itemset in sorted(all_frequent.keys(), key=lambda x: (len(x), sorted(x))):
        print(' '.join(sorted(itemset)))

if __name__ == "__main__":
    main()