from core.option import Option, OptionType, OptionStyle
from core.market import MarketEnvironment
from models.black_scholes import BlackScholesModel
from models.binomial import BinomialModel

def run_comparison():
    print("--- Model Comparison: European Call Option ---")
    
    # Setup parameters
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.05
    sigma = 0.2
    q = 0.0

    option = Option(S0=S0, K=K, T=T, option_type=OptionType.CALL, style=OptionStyle.EUROPEAN)
    market = MarketEnvironment(r=r, sigma=sigma, q=q)

    # Black-Scholes Price
    bs_model = BlackScholesModel()
    bs_price = bs_model.price(option, market)
    print(f"Black-Scholes Price: {bs_price:.6f}")

    # Binomial Model Convergence
    print("\n--- Binomial Convergence ---")
    steps_list = [10, 50, 100, 500, 1000]
    for steps in steps_list:
        bin_model = BinomialModel(steps=steps)
        bin_price = bin_model.price(option, market)
        error = abs(bin_price - bs_price)
        print(f"Steps: {steps:4d} | Price: {bin_price:.6f} | Error: {error:.6f}")

    print("\n--- American vs European Put (Early Exercise) ---")
    # American put should be worth more than European put if early exercise is optimal
    # Deep in the money put: S=80, K=100
    option_eu = Option(S0=80, K=100, T=1.0, option_type=OptionType.PUT, style=OptionStyle.EUROPEAN)
    option_am = Option(S0=80, K=100, T=1.0, option_type=OptionType.PUT, style=OptionStyle.AMERICAN)
    
    # Use Binomial for both to compare style effect
    bin_model = BinomialModel(steps=100)
    
    price_eu = bin_model.price(option_eu, market)
    price_am = bin_model.price(option_am, market)
    
    print(f"European Put Price (Binomial): {price_eu:.6f}")
    print(f"American Put Price (Binomial): {price_am:.6f}")
    print(f"Early Exercise Premium:        {price_am - price_eu:.6f}")

if __name__ == "__main__":
    run_comparison()
