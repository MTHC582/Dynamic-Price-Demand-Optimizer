# Dynamic Pricing and Demand Optimization Simulator with Scenario Analysis

## 1. Problem Definition
In real-world industries such as ticketing, e-commerce, and transportation, pricing decisions significantly impact revenue and inventory utilization. Traditional static pricing fails to adapt to changing market conditions such as fluctuating demand, limited inventory, and time-based urgency.

This project aims to design and implement a dynamic pricing simulation system that models demand uncertainty and evaluates different pricing strategies to maximize revenue and optimize inventory usage.

## 2. Motivation & Issues Addressed
### Problems with Static Pricing:
- Does not respond to demand fluctuations
- Leads to unsold inventory or missed revenue
- Cannot handle uncertainty in customer behavior

### Issues Addressed:
- Adapting pricing dynamically based on demand
- Handling uncertainty using probabilistic simulation
- Improving revenue through better decision strategies
- Understanding which strategy performs best under different conditions

## 3. Core Features
- **Demand Modeling:** Uses price elasticity and aggregate demand logic.
- **Customer Segmentation:** Simulates Budget, Regular, and Urgent buyers with varying price sensitivities.
- **Stochastic Simulation:** Uses Poisson distributions to model random customer arrivals.
- **Multiple Pricing Strategies:**
  - **Static:** Fixed price baseline.
  - **Dynamic:** Reactive pricing based on inventory thresholds.
  - **Advanced:** High-complexity strategy balancing inventory pressure, time scarcity, and scarcity premiums.
- **Multi-Scenario Analysis:** Evaluates strategy robustness across Low Demand, High Demand, and High Sensitivity markets.
- **Automated Reporting:** Generates data-driven insights, revenue improvement calculations, and sensitivity analysis.
- **Data Export:** Saves detailed results to CSV and generates visualization graphs (Revenue, Price, Inventory).

## 4. Technologies Used
- **Python 3.x**
- **Matplotlib:** Data visualization
- **Pandas:** Data manipulation and CSV logging
- **NumPy:** Stochastic modeling (Poisson distribution)
- **JSON:** Configuration management

## 5. Project Structure
```text
project/
├── main.py              # Entry point & Scenario Runner
├── models/
│   ├── market.py        # MarketEnvironment & Customer Segmentation
│   └── strategies.py    # PricingStrategy Pattern Implementation
├── simulation/
│   └── simulator.py     # Core Simulation Engine
├── analysis/
│   └── analysis.py      # Automated Report Generator & Visualization
├── utils/
│   └── helpers.py       # Configuration loading utilities
├── data/
│   └── config.json      # Simulation parameters
└── output/              # Results, CSVs, and Graphs
```

## 6. How to Run
1. Ensure you have the required libraries installed:
   ```bash
   pip install pandas matplotlib numpy
   ```
2. Execute the simulation:
   ```bash
   python main.py
   ```

## 7. Key Concepts Covered
- **Probability & Randomness:** Poisson processes for customer arrivals.
- **Microeconomics:** Price elasticity of demand (PED) modeling.
- **Software Engineering:** Strategy Design Pattern for extendibility and clean code.
- **Optimization:** Revenue management and inventory depletion optimization.
- **Data Science:** Sensitivity analysis and automated insight generation.

## 8. Conclusion
The system demonstrates that adaptive pricing strategies significantly outperform static approaches in uncertain environments. By combining simulation, analysis, and optimization, it provides a robust framework for evaluating real-world pricing decisions.
