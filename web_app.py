from flask import Flask, render_template, request
from core.option import Option, OptionType, OptionStyle
from core.market import MarketEnvironment
from models.black_scholes import BlackScholesModel
from models.binomial import BinomialModel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Default values
    form_values = {
        "S0": 100.0,
        "K": 100.0,
        "T": 1.0,
        "r": 0.05,
        "sigma": 0.2,
        "q": 0.0,
        "option_type": "call",
        "style": "european",
        "model": "bs"
    }
    
    price = None
    greeks = None
    error_message = None
    model_name = ""

    if request.method == "POST":
        try:
            # Update form values from request
            form_values["S0"] = float(request.form.get("S0"))
            form_values["K"] = float(request.form.get("K"))
            form_values["T"] = float(request.form.get("T"))
            form_values["r"] = float(request.form.get("r"))
            form_values["sigma"] = float(request.form.get("sigma"))
            form_values["q"] = float(request.form.get("q"))
            form_values["option_type"] = request.form.get("option_type")
            form_values["style"] = request.form.get("style")
            form_values["model"] = request.form.get("model")

            # Validation
            if form_values["T"] <= 0:
                raise ValueError("Time to maturity must be positive.")
            if form_values["sigma"] < 0:
                raise ValueError("Volatility must be non-negative.")
            if form_values["S0"] < 0 or form_values["K"] < 0:
                raise ValueError("Prices must be non-negative.")

            # Create objects
            option_type = OptionType(form_values["option_type"])
            option_style = OptionStyle(form_values["style"])
            
            option = Option(
                S0=form_values["S0"],
                K=form_values["K"],
                T=form_values["T"],
                option_type=option_type,
                style=option_style
            )
            
            market = MarketEnvironment(
                r=form_values["r"],
                sigma=form_values["sigma"],
                q=form_values["q"]
            )

            # Select model
            if form_values["model"] == "bs":
                pricing_model = BlackScholesModel()
                model_name = "Black-Scholes Model"
            elif form_values["model"] == "binomial":
                pricing_model = BinomialModel()
                model_name = "Binomial Model"
            else:
                raise ValueError("Invalid pricing model selected.")

            # Calculate price
            price = pricing_model.price(option, market)
            
            # Calculate Greeks (if supported)
            try:
                greeks = pricing_model.greeks(option, market)
            except NotImplementedError:
                greeks = None
            except Exception:
                # Some models might return None or raise error if greeks not supported for specific case
                greeks = None

        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"

    return render_template(
        "index.html",
        form_values=form_values,
        price=price,
        greeks=greeks,
        error_message=error_message,
        model_name=model_name
    )

if __name__ == "__main__":
    app.run(debug=True)
