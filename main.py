import sys
from core.option import OptionStyle
from models.black_scholes import BlackScholesModel
from models.binomial import BinomialModel
from ui.cli import get_inputs, display_results

def main():
    try:
        # 1. Get inputs
        option, market, model_choice = get_inputs()

        # 2. Select Model
        if model_choice == "bs":
            if option.style == OptionStyle.AMERICAN:
                print("\n[WARNING] Black-Scholes does not support American options. Switching to European style for pricing.")
                option.style = OptionStyle.EUROPEAN
            
            model = BlackScholesModel()
        else:
            steps = 100
            # Optional: ask for steps if binomial
            # steps = get_float_input("Binomial Steps", 100)
            model = BinomialModel(steps=steps)

        # 3. Calculate Price
        price = model.price(option, market)
        
        # 4. Calculate Greeks (if supported)
        greeks = model.greeks(option, market)

        # 5. Display Results
        display_results(price, greeks)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
