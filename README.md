# Natural Selection Simulator

A Python-based ecosystem simulator inspired by [Primer's videos on natural selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). 

This project explores population dynamics, carrying capacity, and resource competition in a simulated 2D environment. Recently, it has been upgraded to include **NeuroEvolution**, allowing organisms to learn how to survive rather than relying on hardcoded behavior.

## 🧬 How It Works

The core simulation runs on a few simple rules:
1. **Resources:** Every "day", a set amount of food is scattered across the map.
2. **Survival of the Fittest:** At the end of the day:
   - 🟢 **2+ food items:** The organism survives and reproduces (2 organisms spawn the next day).
   - 🟡 **1 food item:** The organism survives to the next day.
   - 🔴 **0 food items:** The organism starves and dies.

By adjusting the initial parameters, we can observe how the population naturally finds its carrying capacity over multiple generations. This environment is not used for the natural selection itself as it is handled by [NEAT](https://neat-python.readthedocs.io/en/latest/)

## Demo

Here is what you are able to get from the simulation at the moment:

1. Training
<img width="600" alt="image showing species' fitness" src="https://github.com/user-attachments/assets/727c9369-83a9-4683-bf5b-e0aca2d04e18" />

> The training is summarized in the form of an image. In the case of the image above, you can see that the fitness plateaued quickly, meaning that the species reached their optimal "thinking" for the given conditions. Let's see what that thinking is

2. Simulation

https://github.com/user-attachments/assets/13804cda-b907-47dc-a3f5-70800b0f9ed2

<img width="600" alt="image" src="https://github.com/user-attachments/assets/eaf5e7e2-684f-4b93-96a7-ff37a90f975f" />

> As you can see, when the food is not recovered immediately, the performance is not stellar. Noticeably, when the organism cannot detect any food, they default to doing "donuts." Theoretically, training in an environment with sparser food distribution can solve this issue.

## 🧠 Technical Features

- **NeuroEvolution (NEAT):** Organisms are controlled by a Neural Network powered by `neat-python`. The network takes in sensory data (vision distance, angles, and speed) and outputs continuous motor controls (acceleration and steering). The networks evolve over generations to optimize hunting strategies.
- **QuadTree Spatial Partitioning:** To support denser population ecosystems efficiently, the simulator relies on a QuadTree data structure for $O(n \log n)$ collision detection and visual range-finding.
- **Trigonometric Physics:** Organisms calculate relative food angles using `atan2` and steer dynamically using `sin/cos` velocity vectors.
- **Data Visualization:** Real-time Matplotlib integration that tracks population carrying-capacity, genetic lineages, and species branching in live charts alongside the Pygame physics simulation.

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
3. **Train the Neural Networks:**
   ```bash
   uv run python -m Simulator
   ```
4. **Debug & Visualize:**
   ```bash
   # Watch the Champion's Neural Network navigate the 2-1-0 sandbox
   uv run python debugging_scripts/watch_champion.py
   
   # Plot the genetic lineages and species branching over time
   uv run python debugging_scripts/plot_stats.py
   ```
5. **Run the tests:**
   ```bash
   uv run pytest tests/
   ```
