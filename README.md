# Dynamic Price and Demand Optimizer

## Problem Statement
Finding the optimal price for a product over time is challenging when inventory is fixed, customer demand fluctuates, and the specific selling period is limited. Maintaining a static price often leads to either selling out inventory too early or being left with excess stock at the end of a product cycle. 

## Utility
This project provides a simulation environment to model various pricing strategies against dynamic market conditions. By mimicking different customer price sensitivities and random demand intervals, the system demonstrates how dynamic pricing can effectively optimize total revenue and inventory clearance when compared to standard stationary pricing models.

This is especially useful to visualize the output as you can tweak parameters in real-time, by changing them either in the `config.json` file or via the Streamlit dashboard mentioned below.

<<<<<<< HEAD
## Pricing Strategies Implemented
* **Static Pricing:** Keeps the price exactly the same throughout the simulation. Used as a simple baseline for comparison.
* **Dynamic Pricing:** Automatically adjusts the price by checking the ratio of how much time is left versus how much stock is left.
* **Advanced Pricing:** Calculates an "urgency score" to apply deep discounts if there is way too much stock, or higher markups if inventory is quickly running out.
=======
>>>>>>> 24590fb6adcb006678e2ae70878488792d240188
## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MTHC582/Dynamic-Price-Demand-Optimizer
cd Dynamic-Price-Demand-Optimizer
```

<<<<<<< HEAD
### 2. Create and Activate a Virtual Environment
It is highly recommended to create and activate a virtual environment before installing dependencies, to prevent conflicts with your system packages.

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements
=======
### NOTE: Suggested to create and activate a virtual environment

### 2. Install Requirements
>>>>>>> 24590fb6adcb006678e2ae70878488792d240188
```bash
pip install -r requirements.txt
```

## Running the Application

There are two separate ways to operate the simulator: through a standard terminal interface or via an interactive web dashboard.

### Command Line Execution
To run a fast background simulation that outputs results and graphs, use the following bash command:
```bash
python main.py
```
*Note: If you have this project loaded in an IDE (such as VSCode or PyCharm), you can also execute this by running the `main.py` file directly within your editor.*

### Streamlit Dashboard
#### "This was added on a later run"  
If you prefer a visual interface where you can experiment with parameter adjustments through interactive sliders, run the Streamlit application:
```bash
streamlit run app.py
```

## Final Directory Structure
After cloning, installing dependencies, and running the simulation (`main.py`) at least once, your final repository structure should resemble the format below:

```text
Dynamic-Price-Demand-Optimizer/
|-- core/
|   |-- analysis.py
|   |-- market.py
|   |-- simulator.py
|   |-- strategies.py
|-- output/
|   |-- graphs/
|   |   |-- price_over_time.png
|   |   |-- revenue_vs_time.png
|   |   |-- strategy_comparison.png
|   |-- results.csv
|-- app.py
|-- main.py
|-- config.json
|-- requirements.txt
|-- README.md
```
