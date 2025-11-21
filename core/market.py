from dataclasses import dataclass

@dataclass
class MarketEnvironment:
    """
    Represents the market environment for option pricing.
    
    Attributes:
        r: Risk-free interest rate (annualized, e.g., 0.05 for 5%).
        sigma: Volatility of the underlying asset (annualized standard deviation).
        q: Continuous dividend yield (default 0.0).
    """
    r: float
    sigma: float
    q: float = 0.0
