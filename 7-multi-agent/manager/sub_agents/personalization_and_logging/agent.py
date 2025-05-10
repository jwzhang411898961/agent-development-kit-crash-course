from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent


# def get_stock_price(ticker: str) -> dict:
#     """Retrieves current stock price and saves to session state."""
#     print(f"--- Tool: get_stock_price called for {ticker} ---")

#     try:
#         # Fetch stock data
#         stock = yf.Ticker(ticker)
#         current_price = stock.info.get("currentPrice")

#         if current_price is None:
#             return {
#                 "status": "error",
#                 "error_message": f"Could not fetch price for {ticker}",
#             }

#         # Get current timestamp
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         return {
#             "status": "success",
#             "ticker": ticker,
#             "price": current_price,
#             "timestamp": current_time,
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "error_message": f"Error fetching stock data: {str(e)}",
#         }


# Create the root agent
stock_analyst = Agent(
    name="personalization_and_logging",
    model="gemini-2.0-flash",
    description="This agent acts as the system's memory and learning component. It stores user preferences and logs key events (like overwhelm instances and strategy effectiveness) to personalize the experience over time, suggest more effective interventions, and provide insights to users or caregivers.",
    instruction="""
    Personalization & Logging Agent:
        Responsibilities:
            Stores and manages user preferences (favorite calming techniques, sensory settings, common triggers if identified).
            Logs event data: overwhelm triggers, chosen strategies, duration of calming, user feedback on strategies, re-engagement success.
            Analyzes logged data (simple analysis) to suggest more effective strategies over time.
            Provides an interface (perhaps for a caregiver) to review logs and adjust preferences.
            Communication: Provides data to Root Agent for decision-making. Receives log data from other agents.
    """,
    # tools=[get_stock_price],
)
