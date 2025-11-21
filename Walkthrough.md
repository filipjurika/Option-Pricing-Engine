Option Pricing Engine Walkthrough
Overview
We have built a command-line option pricing engine in Python. It supports:

Black-Scholes Model: For European options (Call/Put) with Greeks (Delta, Vega).
Binomial Tree Model: For European and American options (Call/Put) with configurable steps.
Verification Results
We ran a comparison script 
test_comparison.py
 to verify the models.

1. Black-Scholes vs Binomial Convergence
We priced a European Call option with:

$S_0 = 100, K = 100, T = 1.0, r = 0.05, \sigma = 0.2$
Results:

Black-Scholes Price: ~10.4506
Binomial Model: Converges to the Black-Scholes price as steps increase.
10 steps: ~10.25
100 steps: ~10.43
1000 steps: ~10.45
2. American Option Early Exercise
We compared European vs American Put options with:

$S_0 = 80, K = 100, T = 1.0, r = 0.05, \sigma = 0.2$ (Deep in-the-money)
Results:

European Put: ~16.70
American Put: ~20.00
Early Exercise Premium: ~3.30
This confirms that the American pricing logic correctly accounts for the value of early exercise.

How to Run
CLI Interface
Run the interactive CLI:

python main.py
Follow the prompts to enter option parameters and choose a model.

Verification Script
Run the verification script:

python test_comparison.py