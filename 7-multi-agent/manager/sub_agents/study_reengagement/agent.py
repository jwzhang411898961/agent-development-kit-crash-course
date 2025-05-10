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
study_reengagement = Agent(
    name="study_reengagement",
    model="gemini-2.0-flash",
    description="This agent facilitates a smooth and encouraging transition back to study tasks after a student has completed a calming activity. It presents supportive options for re-engagement, offers positive reinforcement, and communicates the student's readiness (or need for more time) back to the Root Agent.",
    instruction="""
    Study Reengagement Agent:
        Responsibilities:
            Offers a structured way to transition back to studying after a calming period.
            Presents options like: "Ready to go back?", "Need 5 more minutes?", "Try an easier part of the task?".
            Provides positive reinforcement and encouragement.
            (Optional) Interface with a simple task list or study timer.
            Communication: Activated by Root Agent. Sends "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals to Root Agent.
    """,
    # tools=[get_stock_price],
)
