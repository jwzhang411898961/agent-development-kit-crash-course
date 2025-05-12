from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent

def store_user_preference(preference_type: str, value) -> dict:
    """
    When "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals are sent to Root Agent, it stores or updates a user preference (e.g., favorite strategy, preferred visuals, sound settings).

    Parameters:
    - preference_type (str): The type of preference (e.g., 'calming_strategy', 'visual_theme').
    - value (Any): The value to be stored (e.g., 'breathing', 'dark mode').

    Returns:
    - dict: Confirmation of stored preference.
    """
    return {
        "event": "USER_PREFERENCE_UPDATED",
        "preference_type": preference_type,
        "value": value
    }

def log_event(event_type: str, metadata: dict) -> dict:
    """
    When "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals are sent to Root Agent, it logs an event related to the user's experience (e.g., overwhelm trigger, strategy use, feedback).

    Parameters:
    - event_type (str): Type of event (e.g., 'OVERWHELM_TRIGGERED', 'STRATEGY_USED', 'FEEDBACK_RECEIVED').
    - metadata (dict): Additional information about the event (e.g., timestamp, strategy_name, rating).

    Returns:
    - dict: Acknowledgment that the log entry was accepted.
    """
    return {
        "event": "EVENT_LOGGED",
        "event_type": event_type,
        "data": metadata
    }

def get_user_profile_summary() -> dict:
    """
    When "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals are sent to Root Agent, it returns a summary of user preferences and historical trends for caregiver or system use.

    Returns:
    - dict: Aggregated summary of preferences and outcomes.
    """
    # Placeholder: in real use, would pull from a datastore or cache.
    return {
        "event": "USER_PROFILE_SUMMARY",
        "favorite_strategies": ["breathing", "music"],
        "common_triggers": ["math tasks", "long reading sessions"],
        "effective_strategies_by_trigger": {
            "math tasks": "breathing",
            "long reading sessions": "picture view"
        },
        "reengagement_success_rate": 0.83
    }

def suggest_next_strategy(trigger_context: str) -> dict:
    """
    When "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals are sent to Root Agent, it suggests a calming strategy based on logged context and outcomes.

    Parameters:
    - trigger_context (str): The recent trigger or user situation (e.g., 'after_quiz', 'loud_noise').

    Returns:
    - dict: Recommended strategy.
    """
    # This is where simple logic/ML could be applied in a real implementation
    suggested = "breathing" if "quiz" in trigger_context else "music"
    return {
        "event": "STRATEGY_SUGGESTION",
        "trigger": trigger_context,
        "suggested_strategy": suggested
    }



# Create the sub agent
personalization_and_logging = Agent(
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
        Communication: 
            Provides data to Root Agent for decision-making. Receives log data from other agents.
    """,
    tools=[store_user_preference, log_event, get_user_profile_summary, suggest_next_strategy]
)
