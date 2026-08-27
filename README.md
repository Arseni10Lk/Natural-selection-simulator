# Natural Selection Simulator

A minimalist, Python-based ecosystem simulator inspired by [Primer's videos on natural selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). 

This is a small conceptual toy built to explore population dynamics, carrying capacity, and resource competition in a simulated 2D environment.

## 🧬 How It Works

The simulation runs on a few simple rules:
1. **Resources:** Every "day", a set amount of food is randomly distributed across the map. The amount of food available fluctuates based on the consumption of previous days.
2. **Organisms:** Creatures are spawned at the edges of the map and wander randomly. If they detect food within their vision radius, they will dynamically change direction to pursue it.
3. **Survival of the Fittest:** At the end of the day:
   - 🟢 **2+ food items:** The organism survives and reproduces (2 organisms spawn the next day).
   - 🟡 **1 food item:** The organism survives to the next day.
   - 🔴 **0 food items:** The organism starves and dies.

## 📊 Demos

By adjusting the initial parameters, we can observe how the population naturally finds its carrying capacity.

**Single Run Fluctuation:**
A single simulation can be highly volatile due to random chance. 

https://github.com/user-attachments/assets/1396914d-4306-485e-809b-de952b5b85bf

**Finding the True Carrying Capacity (20 Runs):**
Averaging the results over multiple runs smooths out the fluctuations and reveals the true carrying capacity of the environment.

https://github.com/user-attachments/assets/7ecd82bf-d6f6-43df-93c9-6432e7ed5acf

## 🚀 Installation & Usage

This project uses `uv` for fast, reproducible dependency management.

1. **Install `uv`** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Clone the repository:**
   ```bash
   git clone https://github.com/Arseni10Lk/Natural-selection-simulator.git
   cd Natural-selection-simulator
   ```
3. **Run the simulation:**
   ```bash
   uv run python -m Simulator
   ```
4. **Run the tests:**
   ```bash
   uv run pytest tests/
   ```
