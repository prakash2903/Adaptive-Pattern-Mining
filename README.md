# 🧠 VSW-SCPS: Adaptive Frequent Itemset Mining with Concept Drift Detection

This project implements **VSW-SCPS** (Variable-Sliding Window with SCPS-tree), a dynamic and adaptive frequent itemset mining algorithm for streaming data. It supports **automatic window resizing**, **concept drift detection**, and **frequent pattern mining**, all visualized through a **Streamlit dashboard**.

---

## 📌 Features

- ✅ Real-time mining from transaction streams
- ✅ Automatic **concept drift detection**
- ✅ Dynamic **tree-based storage** (SCPS-tree)
- ✅ Adaptive window resizing (no fixed window size!)
- ✅ Mining of frequent itemsets (up to k=3)
- ✅ Visualization with Streamlit:
  - Top-K patterns per pane
  - Drift rate timeline
- ✅ Two dataset modes:
  - Built-in 50-row synthetic stream (for debug/demos)
  - Real-world Online Retail dataset (UCI)

---

## 📚 Background

This project is based on the paper:

> **"VSW-SCPS: An Adaptive Frequent Itemset Mining Method Based on a Variable-Sliding Window"**  
> DOI: [10.1109/ACCESS.2020.3026813](https://pubs.aip.org/aip/acp/article/1839/1/020146/845849/A-variable-size-sliding-window-based-frequent)

We reimplemented the proposed SCPS-tree and mining logic in Python with an interactive UI.

---

## 🚀 Quick Start

### 🔧 Install Dependencies

```bash
pip install -r requirements.txt
