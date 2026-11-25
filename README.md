# ShopSmart: Inventory and Billing System with Sales Analysis for Small Shops

**Author:** Pranav Gupta (`S26CSEU0676`, Batch 92)  
**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**University:** Bennett University — School of Computer Science Engineering and Technology  
**Academic Year:** 2026–27 (Milestone 2 Project)

## Overview
**ShopSmart** is a menu-driven Python application built for small neighborhood retail stores (grocery, stationery, and general stores). It replaces error-prone manual notebooks with persistent CSV stock management, validated multi-item customer billing, automated low-stock alerts, 30-day sales velocity analysis, and Matplotlib visualizations.

## Repository Structure
- `shopsmart.py` — Complete Python application (OOP classes, inventory CRUD, billing, low-stock alerts, sales analysis, and reporting)
- `inventory.csv` — Persistent inventory records (`item_id, name, category, price, quantity, reorder_level`)
- `sales.csv` — Timestamped customer transaction history


## Key Features
- **O(1) Dictionary & CSV Persistence:** Syncs inventory and sales logs automatically across sessions.
- **Object-Oriented Design:** Uses `Item` and `GroceryItem` classes with `@property` encapsulation and inheritance.
- **Defensive Billing Validation:** Blocks unknown item IDs, non-positive quantities, and orders exceeding available stock.
- **Automated Low-Stock Alerts:** Flags items where `quantity <= reorder_level` using a list comprehension.
- **Computational Sales Analysis:** Ranks products by revenue and units sold, flags 30-day slow-moving items (< 10 units), and summarizes category revenue shares.

## How to Run
```bash
python shopsmart.py
