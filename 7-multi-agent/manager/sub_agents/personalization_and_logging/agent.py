from datetime import datetime

from google.adk.agents import Agent

def log_event(event_type: str, metadata: dict) -> str:
    """
    Logs an event such as overwhelm trigger, strategy used, or feedback.

    Parameters:
        event_type (str): Type of event (e.g., "OVERWHELM_TRIGGERED", "CALMING_DONE", "FEEDBACK_RECEIVED").
        metadata (dict): Additional details about the event (e.g., timestamp, strategy_name, success_rating).

    Returns:
        str: Confirmation message.
    """
    return f"Event '{event_type}' logged successfully with metadata: {metadata}"

def update_user_preferences(preference_type: str, value: str) -> str:
    """
    Updates a user preference such as favorite strategy or sensory setting.

    Parameters:
        preference_type (str): Preference key (e.g., "favorite_strategy", "color_theme").
        value (str): New preference value.

    Returns:
        str: Confirmation of update.
    """
    return f"Preference '{preference_type}' updated to '{value}'."

def get_personalized_suggestion() -> dict:
    """
    Analyzes log data to suggest the most effective calming strategy.

    Returns:
        dict: A suggested strategy with reasoning (if available).
    """
    # This is a placeholder; real logic would analyze stored logs
    return {
        "suggested_strategy": "breathing_exercise",
        "confidence": "high",
        "reason": "This strategy has the highest success feedback in recent sessions."
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
    tools=[log_event, update_user_preferences, get_personalized_suggestion]
)
