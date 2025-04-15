import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_stream import preprocess_data, download_dataset, get_stream_panes
from scps_tree import SCPSTree
from drift_detector import detect_concept_drift
from miner import mine_frequent_itemsets
from visualizer import DriftTracker, plot_frequent_itemsets

# === Streamlit Page Setup ===
st.set_page_config(page_title="VSW-SCPS Miner", layout="wide")
st.title("🧠 VSW-SCPS: Adaptive Frequent Itemset Miner")

# === Sidebar Config ===
st.sidebar.header("⚙️ Parameters")
pane_size = st.sidebar.slider("Pane Size", min_value=5, max_value=100, value=10, step=5)
min_support = st.sidebar.slider("Min Support", min_value=1, max_value=10, value=2)
drift_threshold = st.sidebar.slider("Drift Threshold", min_value=0.1, max_value=1.0, value=0.3, step=0.05)
init_window_panes = st.sidebar.number_input("Initial Window (panes)", min_value=1, max_value=10, value=1)

# === Dataset Choice ===
dataset_choice = st.sidebar.radio("Dataset", ["Test Dataset (50 txns)", "Online Retail (real)"])

# === Load Dataset ===
if dataset_choice == "Test Dataset (50 txns)":
    def preprocess_data(_):
        return [
            ['milk', 'bread', 'butter'], ['milk', 'bread'], ['milk', 'butter'], ['bread', 'butter'], ['milk', 'bread'],
            ['bread', 'butter'], ['milk', 'bread'], ['milk', 'butter'], ['milk', 'bread'], ['bread', 'butter'],
            ['milk', 'cereal'], ['bread', 'cereal'], ['milk', 'bread'], ['cereal', 'butter'], ['milk', 'cereal'],
            ['bread', 'butter'], ['cereal', 'bread'], ['milk', 'cereal'], ['milk', 'bread'], ['butter', 'cereal'],
            ['coffee', 'cereal'], ['milk', 'coffee'], ['cereal', 'bread'], ['coffee', 'butter'], ['coffee', 'cereal'],
            ['coffee', 'milk'], ['bread', 'coffee'], ['cereal', 'coffee'], ['cereal', 'milk'], ['butter', 'coffee'],
            ['juice', 'tea'], ['snack', 'juice'], ['tea', 'juice'], ['snack', 'cereal'], ['tea', 'snack'],
            ['tea', 'coffee'], ['juice', 'coffee'], ['juice', 'snack'], ['coffee', 'snack'], ['tea', 'cereal'],
            ['pen', 'notebook'], ['notebook', 'eraser'], ['pen', 'eraser'], ['notebook', 'pencil'],
            ['stapler', 'paper'], ['pen', 'notebook'], ['eraser', 'paper'], ['pen', 'stapler'],
            ['notebook', 'pen'], ['notebook', 'paper']
        ]
    df = None
else:
    df = download_dataset()

transactions = preprocess_data(df)
panes = list(get_stream_panes(transactions, pane_size=pane_size))

# === Start Mining ===
st.subheader("📦 Streaming Results")
tree = SCPSTree()
drift_tracker = DriftTracker()
tid_counter = 0
checkpoint_tid = pane_size * init_window_panes

for pane_index, pane in enumerate(panes):
    st.markdown(f"### ⏳ Pane {pane_index + 1}: Transactions {tid_counter} to {tid_counter + len(pane) - 1}")

    for transaction in pane:
        tree.insert_transaction(transaction, checkpoint_tid, tid_counter)
        tid_counter += 1

    drift_triggered = detect_concept_drift(tree, min_support, threshold=drift_threshold)
    drift_tracker.log_drift(pane_index + 1, int(drift_triggered), drift_triggered)

    if drift_triggered:
        st.warning(f"⚠️ Concept drift detected at Pane {pane_index + 1}! Tree shrinking applied.")
        tree.delete_expired_data()
        checkpoint_tid = tid_counter
    else:
        st.success("✅ No significant drift. Window grows.")

    # Show frequent itemsets
    frequent_itemsets = mine_frequent_itemsets(tree, min_support=min_support, max_length=3)
    df_patterns = pd.DataFrame([(tuple(k), v) for k, v in frequent_itemsets.items()], columns=["Itemset", "Support"])
    df_patterns = df_patterns.sort_values("Support", ascending=False)

    st.write(f"🧠 Top Frequent Itemsets (min support = {min_support}):")
    st.dataframe(df_patterns.head(10), use_container_width=True)

    # Plot bar chart
    if not df_patterns.empty:
        fig, ax = plt.subplots()
        df_patterns.head(10).plot(kind='bar', x='Itemset', y='Support', ax=ax, legend=False)
        plt.title(f"Top Frequent Itemsets - Pane {pane_index + 1}")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

# === Plot drift rate over time ===
st.subheader("📈 Concept Drift Rate Over Time")
fig_drift, ax = plt.subplots()
ax.plot(drift_tracker.pane_numbers, drift_tracker.drift_rates, marker='o', label="Drift Rate")
for i, triggered in enumerate(drift_tracker.drift_flags):
    if triggered:
        ax.axvline(x=drift_tracker.pane_numbers[i], color='red', linestyle='--', alpha=0.6)
ax.set_xlabel("Pane Number")
ax.set_ylabel("Drift Triggered")
ax.set_title("Concept Drift Detection Timeline")
ax.grid(True)
st.pyplot(fig_drift)
