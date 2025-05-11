from data_stream import download_dataset 
from data_stream import preprocess_data
from data_stream import get_stream_panes
from scps_tree import SCPSTree
from drift_detector import detect_concept_drift
from miner import mine_frequent_itemsets
from visualizer import DriftTracker
from visualizer import plot_frequent_itemsets

# Configurations
PANE_SIZE = 5
INIT_WINDOW_SIZE = 1  # number of panes
MIN_SUPPORT = 2
DRIFT_THRESHOLD = 0.3

def main():
    print("⏬ Loading data...")
    df = download_dataset()
    transactions = preprocess_data(df)
    panes = get_stream_panes(transactions, pane_size=PANE_SIZE)

    tree = SCPSTree()
    tid_counter = 0
    checkpoint_tid = INIT_WINDOW_SIZE * PANE_SIZE
    drift_tracker = DriftTracker()

    print("🚀 Starting VSW-SCPS streaming...")
    for pane_index, pane in enumerate(panes):
        print(f"\n📦 Inserting Pane {pane_index + 1} (Transactions {tid_counter} to {tid_counter + len(pane) - 1})")
        for transaction in pane:
            tree.insert_transaction(transaction, checkpoint_tid, tid_counter)
            tid_counter += 1

        print("🌳 Tree after pane insertion:")
        tree.print_tree()

        # Concept Drift Detection and Window Adjustment
        drift_rate = 0
        drift_triggered = detect_concept_drift(tree, MIN_SUPPORT, threshold=DRIFT_THRESHOLD)
        
        if drift_triggered:
            print("🔁 Concept drift detected! Shrinking window...")
            tree.delete_expired_data()
            checkpoint_tid = tid_counter
            drift_rate = 1
        
        else:
            print("✅ No significant drift. Window can grow.")

        drift_tracker.log_drift(pane_index + 1, drift_rate, drift_triggered)

        # Show frequent itemsets
        frequent_itemsets = mine_frequent_itemsets(tree, MIN_SUPPORT, max_length=3)
        print(f"🧠 Mined {len(frequent_itemsets)} frequent itemsets (support ≥ {MIN_SUPPORT}):")
        
        for itemset, support in sorted(frequent_itemsets.items(), key=lambda x: -x[1])[:10]:
            print(f"  {itemset} -> {support}")

        plot_frequent_itemsets(frequent_itemsets)

        '''
        if pane_index == 0:
            print("Demo stopped after 6 panes.")
            break
        '''
        
    # Show drift rate over time
    drift_tracker.plot_drift()

if __name__ == "__main__":
    main()
