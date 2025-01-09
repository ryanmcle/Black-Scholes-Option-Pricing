# Black-Scholes Option Pricing Model

## Description
A Python application that implements the **Black-Scholes option pricing model** for European call and put options. The system allows users to input stock tickers, select expiration dates and strike prices, and compute the option price based on real-time stock data and historical volatility. The project utilizes **yfinance** to fetch real-time stock data and computes the option price based on market conditions.

## Features

- **Option Pricing**: Calculate the price of European call and put options using the Black-Scholes formula.
- **Real-Time Stock Data**: Fetch current stock price, historical volatility, and option chain data using the **yfinance** API.
- **Expiration Date Selection**: Select an expiration date from available options for the given stock ticker.
- **Strike Price Selection**: Choose strike prices from the available options chain data.
- **Historical Volatility**: Automatically calculate the volatility of the underlying stock from historical price data.
- **Risk-Free Rate**: Incorporates a default risk-free interest rate (currently set at 4.5%).
- **Interactive Command-Line Interface**: Simple CLI that allows users to input stock ticker symbols and option details for real-time pricing.

## Video
![Black-Scholes Option Pricing Video](https://github.com/ryanmcle/Black-Scholes-Option-Pricing/blob/main/black_Scholes-ezgif.com-video-to-gif-converter.gif?raw=true) 
Watch the demonstration of the Black-Scholes model applied to real-world stock data.

## Screenshot
![Black-Scholes Screenshot](https://github.com/ryanmcle/Black-Scholes-Option-Pricing/blob/main/black_scholes.png)

This screenshot shows the console output after calculating the price of an option.

## Technologies Used

- **Python 3**: Programming language used to build the application.
- **yfinance**: Python library to fetch real-time stock and option data from Yahoo Finance.
- **NumPy**: Used for numerical calculations, including logarithms and square roots.
- **SciPy**: Used for statistical functions, specifically the cumulative distribution function (CDF) for the standard normal distribution.
- **Datetime**: Python module used to handle time and date calculations for the option expiration.
- **Command-Line Interface (CLI)**: Simple text-based interface for interacting with the user.

## Installation

### Clone the Repository

```bash
git clone https://github.com/ryanmcle/black-scholes-option-pricing.git
