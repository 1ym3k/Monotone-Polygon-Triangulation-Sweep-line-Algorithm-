# Monotone Polygon Triangulation (Sweep-line Algorithm)

This project implements a linear-time triangulation algorithm for $x$-monotone polygons using the **Sweep-line technique**. It was developed as part of the **Combinatorial Optimization** course (Winter Semester 2025/2026).

## 📋 Overview
The goal of this project is to partition a simple, strictly $x$-monotone polygon into triangles by adding non-intersecting internal diagonals.

**Key Features:**
* **Algorithm:** Sweep-line triangulation.
* **Time Complexity:** $O(n)$.
* **Space Complexity:** $O(n)$.
* **Input Data:** Simple polygons defined by vertices in Counter-Clockwise (CCW) order.

## ⚙️ Requirements
* **Language:** Python 3.7+
* **Dependencies:** None (Standard Library only).

## 🚀 Usage

1.  Prepare your input file (e.g., `input.txt`) following the format specification below.
2.  Run the script from the terminal:

```bash
python triangulation.py
