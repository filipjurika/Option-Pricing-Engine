from abc import ABC, abstractmethod
from typing import Dict, Optional
from core.option import Option
from core.market import MarketEnvironment

class PricingModel(ABC):
    """
    Abstract base class for all option pricing models.
    """

    @abstractmethod
    def price(self, option: Option, market: MarketEnvironment) -> float:
        """
        Calculates the price of the option.

        Args:
            option: The option contract to price.
            market: The market environment.

        Returns:
            The calculated option price.
        """
        pass

    def greeks(self, option: Option, market: MarketEnvironment) -> Optional[Dict[str, float]]:
        """
        Calculates the Greeks for the option.

        Args:
            option: The option contract.
            market: The market environment.

        Returns:
            A dictionary containing Greek values (e.g., 'delta', 'vega'), or None if not implemented.
        """
        return None
