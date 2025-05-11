import matplotlib.pyplot as plt

class DriftTracker:
    def __init__(self):
        self.pane_numbers = []
        self.drift_rates = []
        self.drift_flags = []

    def log_drift(self, pane_number, drift_rate, drift_triggered):
        self.pane_numbers.append(pane_number)
        self.drift_rates.append(drift_rate)
        self.drift_flags.append(drift_triggered)

    def plot_drift(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.pane_numbers, self.drift_rates, marker='o', label="Drift Rate")
        
        for i, triggered in enumerate(self.drift_flags):
            if triggered:
                plt.axvline(x=self.pane_numbers[i], color='red', linestyle='--', alpha=0.6)

        plt.title("Concept Drift Rate Over Time")
        plt.xlabel("Pane Number")
        plt.ylabel("Drift Rate")
        plt.ylim(0, 1.1)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_frequent_itemsets(frequent_itemsets, top_n=10):
    """
    Bar chart of top frequent itemsets by support
    """
    top_items = sorted(frequent_itemsets.items(), key=lambda x: -x[1])[:top_n]
    labels = [' '.join(itemset) for itemset, _ in top_items]
    values = [count for _, count in top_items]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(f"Top {top_n} Frequent Itemsets")
    plt.ylabel("Support Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
