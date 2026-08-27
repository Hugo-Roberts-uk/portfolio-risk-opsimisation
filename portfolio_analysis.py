import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "JPM", "KO"]
data = yf.download(tickers,
                   start="2021-01-01",
                   end="2026-01-01",
                   auto_adjust=True,
                   threads=False)
print(data.head())
prices = data["Close"]
print(prices.head())
returns = prices.pct_change()
print(returns.head())
returns = returns.dropna()
print(returns.head())
average_daily_return = returns.mean()
print(average_daily_return)
annual_return = average_daily_return * 252
print(annual_return)
daily_volatility = returns.std()
print(daily_volatility)
annual_volatility = daily_volatility * np.sqrt(252)
print(annual_volatility)
risk_free_rate = 0.03
sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
summary = pd.DataFrame({"Annual Return (%)": annual_return * 100, "Annual Volatility (%)": annual_volatility * 100, "Sharpe Ratio": sharpe_ratio})
print("\n--- STOCK PERFORMANCE SUMMARY ---")
print(summary.round(2))
correlation_matrix = returns.corr()
print("\n--- CORRELATION MATRIX ---")
print(correlation_matrix)
weights = np.array([1/6] * 6)
portfolio_return = np.sum(average_daily_return * weights) * 252
portfolio_volatility = np.sqrt(weights.T @ returns.cov() @ weights) * np.sqrt(252)
portfolio_sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
print("\n--- EQUAl-WEIGHTED PORTFOLIO ---")
print(f"Annual Return: {portfolio_return:.2%}")
print(f"Annual Volatility: {portfolio_volatility:.2%}")
print(f"Sharpe Ratio: {portfolio_sharpe:.2f}")
print("\n Although NVDA generated the highest historical return,"
      " combining the six stocks into an equal-weighted portfolio "
      "produced a lower level of volatility and a stronger "
      "risk-adjusted returns than most individual holdings")

num_portfolios = 5000
portfolio_results = []
for i in range(num_portfolios):
    weights = np.random.random(len(tickers))
    weights = weights / np.sum(weights)
    if np.max(weights) > 0.3:
        continue
    portfolio_return = np.sum(average_daily_return * weights) * 252
    portfolio_volatility = np.sqrt(weights.T @ returns.cov() @ weights) * np.sqrt(252)
    portfolio_sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
    portfolio_results.append([portfolio_return, portfolio_volatility, portfolio_sharpe, weights])
returns_df = pd.DataFrame(portfolio_results, columns=["Return", "Volatility", "Sharpe Ratio", "Weights"])
print("\n---SIMULATED PORTFOLIOS---")
print(returns_df.head())
best_portfolio = returns_df.loc[returns_df["Sharpe Ratio"].idxmax()]
print("\n---BEST SIMULATED PORTFOLIO---")
print(best_portfolio)
best_weights = best_portfolio["Weights"]
weight_table = pd.DataFrame({"Ticker": tickers, "Weights": best_weights})
weight_table["Weight (%)"] = weight_table["Weights"] * 100
print("\n---BEST PORTFOLIO ALLOCATIONS---")
print(weight_table[["Ticker", "Weight (%)"]].round(2))
#---Portfolio Comparison---
comparison = pd.DataFrame({"Portfolio": ["Equal-weighted", "Best Simulated"], "Annual Return (%)":
                            [portfolio_return * 100, best_portfolio["Return"]*100],
                           "Annual Volatility (%)": [portfolio_volatility * 100, best_portfolio["Volatility"]*100],
                           "Sharpe Ratio": [portfolio_sharpe, best_portfolio["Sharpe Ratio"]]})
print("\n--- PORTFOLIO COMPARISON ---")
print(comparison.round(2))
plt.figure(figsize = (10,6))
scatter=plt.scatter(returns_df["Volatility"], returns_df["Return"], c=returns_df["Sharpe Ratio"], cmap="viridis", vmin=0, vmax=best_portfolio["Sharpe Ratio"], alpha=0.5)
#Best Simulated Portfolio
plt.scatter(best_portfolio["Volatility"], best_portfolio["Return"], marker="*", s=300, label="Best portfolio")
#Equal-Weighted Portfolio
plt.scatter(portfolio_volatility, portfolio_return, marker="o", s=150, label="Equal-Weighted Portfolio")
plt.xlabel("Annual Volatility")
plt.ylabel("Annual Return")
plt.title("Monte Carlo Portfolio Simulation")
plt.colorbar(scatter, label="Sharpe Ratio")
plt.legend()
plt.show()
