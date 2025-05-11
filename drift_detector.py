
def mine_frequent_itemsets(tree, min_support, is_after_checkpoint=False):
    """
    Extracts frequent 1-itemsets from SCPS-tree with support ≥ min_support
    """
    freq_itemsets = set()

    for item, nodes in tree.head_table.items():
        support = 0
        
        for node in nodes:
            if node.is_tail:
                support += node.cur_count if is_after_checkpoint else node.pre_count
            else:
                support += node.count
        
        if support >= min_support:
            freq_itemsets.add(item)
    
    return freq_itemsets

def compute_drift(old_set, new_set):
    """
    Returns concept drift rate between two sets
    """
    added = new_set - old_set
    removed = old_set - new_set
    total = len(old_set.union(new_set))

    if total == 0:
        return 0.0
    
    return (len(added) + len(removed)) / total

def detect_concept_drift(tree, min_support, threshold=0.3):
    """
    Main concept drift detection function
    """
    old_freq = mine_frequent_itemsets(tree, min_support, is_after_checkpoint=False)
    new_freq = mine_frequent_itemsets(tree, min_support, is_after_checkpoint=True)
    
    drift = compute_drift(old_freq, new_freq)
    print(f"Concept Drift Check: change rate = {drift:.2f}")
    
    return drift > threshold
