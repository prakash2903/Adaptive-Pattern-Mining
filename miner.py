from collections import defaultdict
from itertools import combinations

def mine_frequent_itemsets(tree, min_support, max_length=3):
    """
    Mines frequent itemsets (up to max_length) from SCPS-tree.
    Returns: dict {itemset: support}
    """
    itemset_counts = defaultdict(int)

    # Step 1: Gather paths from each tail node to root
    for item, nodes in tree.head_table.items():
        for node in nodes:
            path = []
            current = node
            
            while current and current.item != "root":
                path.append(current.item)
                current = current.parent

            # root -> leaf
            path = list(reversed(path))

            # Step 2: Generate combinations from this path
            for i in range(1, min(max_length, len(path)) + 1):
                for combo in combinations(path, i):
                    itemset_counts[combo] += 1

    # Step 3: Filter by min support
    frequent_itemsets = {itemset: count for itemset, count in itemset_counts.items() if count >= min_support}
    return frequent_itemsets
