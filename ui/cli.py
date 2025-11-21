from typing import Tuple, Optional
from core.option import Option, OptionType, OptionStyle
from core.market import MarketEnvironment

def get_float_input(prompt: str, default: Optional[float] = None) -> float:
    """Gets a float input from the user."""
    while True:
        user_input = input(f"{prompt} [{default}]: " if default is not None else f"{prompt}: ")
        if not user_input and default is not None:
            return default
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_choice_input(prompt: str, choices: list) -> str:
    """Gets a choice input from the user."""
    choices_str = "/".join(choices)
    while True:
        user_input = input(f"{prompt} ({choices_str}): ").lower().strip()
        if user_input in choices:
            return user_input
        print(f"Invalid input. Please choose from {choices_str}.")

def get_inputs() -> Tuple[Option, MarketEnvironment, str]:
    """
    Interactively gathers inputs from the user.
    Returns:
        Tuple containing Option, MarketEnvironment, and model choice ('bs' or 'binomial').
    """
    print("\n--- Option Pricing Engine ---")
    print("Please enter the parameters for the option and market.\n")

    # Option parameters
    S0 = get_float_input("Spot Price (S0)", 100.0)
    K = get_float_input("Strike Price (K)", 100.0)
    T = get_float_input("Time to Maturity (T in years)", 1.0)
    
    type_str = get_choice_input("Option Type", ["call", "put"])
    option_type = OptionType.CALL if type_str == "call" else OptionType.PUT
    
    style_str = get_choice_input("Option Style", ["european", "american"])
    style = OptionStyle.EUROPEAN if style_str == "european" else OptionStyle.AMERICAN

    # Market parameters
    r = get_float_input("Risk-free Rate (r, e.g., 0.05)", 0.05)
    sigma = get_float_input("Volatility (sigma, e.g., 0.2)", 0.2)
    q = get_float_input("Dividend Yield (q, e.g., 0.0)", 0.0)

    # Model choice
    model_choice = get_choice_input("Pricing Model", ["bs", "binomial"])

    option = Option(S0=S0, K=K, T=T, option_type=option_type, style=style)
    market = MarketEnvironment(r=r, sigma=sigma, q=q)

    return option, market, model_choice

def display_results(price: float, greeks: Optional[dict] = None):
    """Displays the pricing results."""
    print("\n--- Results ---")
    print(f"Option Price: {price:.4f}")
    
    if greeks:
        print("\nGreeks:")
        for key, value in greeks.items():
            print(f"  {key.capitalize()}: {value:.4f}")
    print("\n----------------")
