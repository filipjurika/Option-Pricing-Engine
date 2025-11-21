import math
from typing import Dict, Optional
from core.option import Option, OptionType, OptionStyle
from core.market import MarketEnvironment
from models.base import PricingModel

class BinomialModel(PricingModel):
    """
    Implementation of the Binomial Tree pricing model.
    Supports both European and American options.
    """

    def __init__(self, steps: int = 100):
        self.steps = steps

    def price(self, option: Option, market: MarketEnvironment) -> float:
        """
        Calculates the option price using a recombining binomial tree.
        """
        S = option.S0
        K = option.K
        T = option.T
        r = market.r
        sigma = market.sigma
        q = market.q
        steps = self.steps
        
        # Handle expiration
        if T <= 1e-9:
            if option.option_type == OptionType.CALL:
                return max(0.0, S - K)
            else:
                return max(0.0, K - S)

        dt = T / steps
        # CRR (Cox-Ross-Rubinstein) parameters
        u = math.exp(sigma * math.sqrt(dt))
        d = 1.0 / u
        p = (math.exp((r - q) * dt) - d) / (u - d)

        # Initialize asset prices at maturity (leaves of the tree)
        # We need steps + 1 nodes
        asset_prices = [0.0] * (steps + 1)
        for i in range(steps + 1):
            asset_prices[i] = S * (u ** (steps - i)) * (d ** i)

        # Initialize option values at maturity
        option_values = [0.0] * (steps + 1)
        for i in range(steps + 1):
            if option.option_type == OptionType.CALL:
                option_values[i] = max(0.0, asset_prices[i] - K)
            else:
                option_values[i] = max(0.0, K - asset_prices[i])

        # Backward induction
        # Discount factor per step
        df = math.exp(-r * dt)

        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                # Continuation value
                continuation = df * (p * option_values[i] + (1 - p) * option_values[i+1])
                
                # Update asset price for this node (re-calculate or store? Re-calculating is easier for memory)
                # Asset price at node (j, i) is S * u^(j-i) * d^i
                current_spot = S * (u ** (j - i)) * (d ** i)

                if option.style == OptionStyle.AMERICAN:
                    # Check for early exercise
                    if option.option_type == OptionType.CALL:
                        exercise = max(0.0, current_spot - K)
                    else:
                        exercise = max(0.0, K - current_spot)
                    option_values[i] = max(continuation, exercise)
                else:
                    option_values[i] = continuation

        return option_values[0]
