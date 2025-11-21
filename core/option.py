from dataclasses import dataclass
from enum import Enum

class OptionType(Enum):
    CALL = "call"
    PUT = "put"

class OptionStyle(Enum):
    EUROPEAN = "european"
    AMERICAN = "american"

@dataclass
class Option:
    """
    Represents a financial option contract.
    
    Attributes:
        S0: Current spot price of the underlying asset.
        K: Strike price of the option.
        T: Time to maturity in years.
        option_type: Type of the option (CALL or PUT).
        style: Style of the option (EUROPEAN or AMERICAN).
    """
    S0: float
    K: float
    T: float
    option_type: OptionType
    style: OptionStyle
