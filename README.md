# Option-Pricing-Engine
Option pricing engine in Python showcasing algorithms, dynamic programming, and Monte Carlo simulation for European and American options.
## Features

- **Option & market models**
  - Dataclasses for options (call/put, European/American) and market environment (r, σ, etc.)
- **Pricing models**
  - Black–Scholes closed-form model for European options
  - Binomial tree model for European and American options (backward induction / dynamic programming)
  - Optional Monte Carlo simulation for European options
- **Risk metrics**
  - Core Greeks (e.g. Delta, Gamma, Vega, Theta, Rho) for Black–Scholes
  - Implied volatility solver using numerical root-finding
- **CS focus**
  - Clean, modular Python design with a shared `PricingModel` interface
  - Simple CLI interface to experiment with parameters
  - Basic tests and comparisons of accuracy and runtime between models
