import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf
from datetime import datetime
from typing import Dict, Any

def black_scholes(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call') -> float:
    """
    Calculate the Black-Scholes option price for European call or put options.
    
    Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to expiration in years
        r (float): Risk-free interest rate (annual)
        sigma (float): Volatility of the underlying stock (annual standard deviation)
        option_type (str): 'call' or 'put'

    Returns:
        float: Option price
    """
    option_type = option_type.lower()
    if option_type not in ['call', 'put']:
        raise ValueError("option_type must be either 'call' or 'put'")

    if sigma <= 0 or T <= 0:
        return max(0.0, S - K) if option_type == 'call' else max(0.0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

def get_historical_volatility(ticker: str, period: str = '1y') -> float:
    """
    Calculate historical volatility of a stock over a given period.
    
    Parameters:
        ticker (str): Stock ticker symbol
        period (str): Period for which to retrieve historical data (e.g., '1y', '6mo')

    Returns:
        float: Annualized volatility
    """
    data = yf.download(ticker, period=period, progress=False)
    if data.empty:
        raise ValueError(f"No historical data found for ticker {ticker}")

    data['Returns'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
    std_dev = data['Returns'].std()
    volatility = std_dev * np.sqrt(252)
    return volatility

def get_option_data(ticker: str) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Fetch option chain data for a given ticker.

    Parameters:
        ticker (str): Stock ticker symbol

    Returns:
        dict: Option expiration dates and options data
    """
    stock = yf.Ticker(ticker)
    expirations = stock.options
    if not expirations:
        raise ValueError(f"No options data available for ticker {ticker}")

    options_data = {}
    for exp in expirations:
        options_chain = stock.option_chain(exp)
        options_data[exp] = {'calls': options_chain.calls, 'puts': options_chain.puts}
    return options_data

def get_risk_free_rate() -> float:
    """
    Retrieve the current risk-free interest rate.

    Returns:
        float: Risk-free interest rate as a decimal
    """
    # Placeholder for fetching the current risk-free rate
    return 0.045  # 4.5% annual risk-free rate

def main():
    print("Black-Scholes Option Pricing Model with Real-Time Data")
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").strip().upper()

    try:
        # Fetch current stock price
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period='1d')
        if stock_data.empty:
            raise ValueError(f"No price data available for ticker {ticker}")
        S = stock_data['Close'][0]
        print(f"Current Stock Price (S): ${S:.2f}")

        # Fetch option data
        option_data = get_option_data(ticker)
        expirations = list(option_data.keys())
        print("\nAvailable Expiration Dates:")
        for idx, exp in enumerate(expirations):
            print(f"{idx + 1}: {exp}")

        # Select expiration date
        exp_index = int(input("Select an expiration date by number: ")) - 1
        expiration_date = expirations[exp_index]
        print(f"Selected Expiration Date: {expiration_date}")

        # Calculate time to expiration in years
        today = datetime.now().date()
        expiration = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        T = (expiration - today).days / 365.0
        if T <= 0:
            raise ValueError("Expiration date must be in the future.")

        # Get strike prices
        option_type_input = input("Option type ('call' or 'put'): ").strip().lower()
        if option_type_input not in ['call', 'put']:
            raise ValueError("Option type must be 'call' or 'put'.")

        options_chain = option_data[expiration_date][option_type_input + 's']
        strike_prices = options_chain['strike'].values
        print("\nAvailable Strike Prices:")
        for idx, strike in enumerate(strike_prices):
            print(f"{idx + 1}: {strike}")

        # Select strike price
        strike_index = int(input("Select a strike price by number: ")) - 1
        K = strike_prices[strike_index]
        print(f"Selected Strike Price (K): ${K:.2f}")

        # Get risk-free rate
        r = get_risk_free_rate()
        print(f"Risk-Free Interest Rate (r): {r * 100:.2f}%")

        # Calculate volatility
        sigma = get_historical_volatility(ticker)
        print(f"Historical Volatility (σ): {sigma * 100:.2f}%")

        # Calculate option price
        option_price = black_scholes(S, K, T, r, sigma, option_type=option_type_input)
        print(f"\n{option_type_input.capitalize()} Option Price: ${option_price:.2f}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
