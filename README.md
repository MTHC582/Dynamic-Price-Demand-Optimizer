# Dynamic Pricing and Demand Simulator

A simulation engine designed to evaluate different pricing strategies across various market conditions and customer segments.

## Overview
This system models a retail environment over a defined simulation period. It allows for the comparison of static and dynamic pricing models by tracking revenue, inventory depletion, and customer demand.

### Features
- **Market Modeling**: Simulates Budget, Regular, and Urgent customer segments with varying price elasticity.
- **Demand Logic**: Uses Poisson distribution to simulate stochastic customer arrivals.
- **Pricing Strategies**:
    - **Static**: Constant price baseline.
    - **Dynamic**: Reactive pricing based on remaining inventory and time metrics.
    - **Advanced**: Heuristic-based pricing using an urgency factor (stock vs. time ratio).
- **Visualization**: Generates cumulative revenue and price trend graphs.
- **Interactive UI**: Includes a Streamlit interface for real-time parameter adjustment.

## Installation
Requires Python 3.x and the following dependencies:

```bash
pip install pandas matplotlib numpy streamlit
```
Or use the provided requirements file:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Mode
To run the simulation using settings from `config.json` and output results to the terminal:
```bash
python main.py
```

### Dashboard Mode
To launch the interactive web interface:
```bash
streamlit run app.py
```

## Project Structure
```text
.
├── core/
│   ├── analysis.py       
│   ├── market.py         
│   ├── simulator.py      
│   └── strategies.py     
├── output/  
│   ├── graphs       
│   └── results.csv                    
├── app.py                
├── main.py               
├── config.json          
├── requirements.txt      
└── README.md
```

