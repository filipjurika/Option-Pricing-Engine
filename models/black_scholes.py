import math
from statistics import NormalDist
from typing import Dict, Optional
from core.option import Option, OptionType, OptionStyle
from core.market import MarketEnvironment
from models.base import PricingModel

class BlackScholesModel(PricingModel):
    """
    Implementation of the Black-Scholes pricing model for European options.
    """

    def _d1_d2(self, option: Option, market: MarketEnvironment):
        """
        Helper to calculate d1 and d2 parameters.
        """
        S = option.S0
        K = option.K
        T = option.T
        r = market.r
        sigma = market.sigma
        q = market.q

        # Avoid division by zero if T is very small
        if T <= 1e-9:
            return 0.0, 0.0

        d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return d1, d2

    def price(self, option: Option, market: MarketEnvironment) -> float:
        """
        Calculates the Black-Scholes price for a European option.
        """
        if option.style != OptionStyle.EUROPEAN:
            raise ValueError("Black-Scholes model only supports European options.")

        S = option.S0
        K = option.K
        T = option.T
        r = market.r
        q = market.q

        # Handle expiration case
        if T <= 1e-9:
            if option.option_type == OptionType.CALL:
                return max(0.0, S - K)
            else:
                return max(0.0, K - S)

        d1, d2 = self._d1_d2(option, market)
        norm = NormalDist()

        if option.option_type == OptionType.CALL:
            # Call price: S * e^(-qT) * N(d1) - K * e^(-rT) * N(d2)
            price = (S * math.exp(-q * T) * norm.cdf(d1) - 
                     K * math.exp(-r * T) * norm.cdf(d2))
        else:
            # Put price: K * e^(-rT) * N(-d2) - S * e^(-qT) * N(-d1)
            price = (K * math.exp(-r * T) * norm.cdf(-d2) - 
                     S * math.exp(-q * T) * norm.cdf(-d1))

        return price

    def greeks(self, option: Option, market: MarketEnvironment) -> Optional[Dict[str, float]]:
        """
        Calculates Delta and Vega for the option.
        """
        if option.style != OptionStyle.EUROPEAN:
            return None

        S = option.S0
        T = option.T
        q = market.q
        
        if T <= 1e-9:
            return {"delta": 0.0, "vega": 0.0}

        d1, _ = self._d1_d2(option, market)
        norm = NormalDist()

        # Delta
        if option.option_type == OptionType.CALL:
            delta = math.exp(-q * T) * norm.cdf(d1)
        else:
            delta = -math.exp(-q * T) * norm.cdf(-d1)

        # Vega (same for call and put)
        # Vega = S * e^(-qT) * N'(d1) * sqrt(T)
        # Note: NormalDist().pdf(x) gives N'(x)
        vega = S * math.exp(-q * T) * norm.pdf(d1) * math.sqrt(T)

        return {
            "delta": delta,
            "vega": vega
        }
