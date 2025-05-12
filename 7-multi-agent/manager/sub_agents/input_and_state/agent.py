from datetime import datetime

# import yfinance as yf
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def calm_beacon_tapped(context: str = "") -> dict:
    """
    Called when the student taps the Calm Beacon (e.g., the persistent 'Need Help?' button).

    Parameters:
    - context (str, optional): Any optional description of what led the user to tap the button.

    Returns:
    - dict: Emits the OVERWHELM_TRIGGERED signal to the Root Agent.
    """
    return {
        "event": "OVERWHELM_TRIGGERED",
        "source": "CalmBeacon",
        "context": context,
        "message": "User signaled feeling overwhelmed by tapping Calm Beacon.",
        "suggestions": ["Pause workflow", "Offer hint", "Open support options"]
    }

def on_overwhelm_gesture_detected(gesture_type: str = "long_press", location: str = "") -> dict:
    """
    Triggered when a recognized gesture (e.g., long press, swipe) is interpreted as a signal for overwhelm.

    Parameters:
    - gesture_type (str): Type of gesture triggering the event.
    - location (str, optional): Screen area or task associated with the gesture.

    Returns:
    - dict: OVERWHELM_TRIGGERED signal.
    """
    return {
        "event": "OVERWHELM_TRIGGERED",
        "source": f"Gesture:{gesture_type}",
        "context": location,
        "message": f"User used gesture '{gesture_type}' to signal overwhelm.",
        "suggestions": ["Pause", "Slow down", "Support options"]
    }

def log_mood_checkin(mood_value: str) -> dict:
    """
    Captures a simple mood selection from the user (emoji or color-coded).

    Parameters:
    - mood_value (str): One of "happy", "okay", "a_little_stressed", "very_overwhelmed"

    Returns:
    - dict: A MOOD_LOGGED event for non-critical states, and optionally OVERWHELM_TRIGGERED if severe.
    """
    events = [{
        "event": "MOOD_LOGGED",
        "mood": mood_value,
        "message": f"User checked in with mood: {mood_value}."
    }]

    if mood_value == "very_overwhelmed":
        events.append({
            "event": "OVERWHELM_TRIGGERED",
            "source": "MoodCheckin",
            "context": mood_value,
            "message": "Mood check-in indicates high overwhelm. Triggering support actions."
        })

    return {"events": events}

def acknowledge_feedback_ui(feedback_type: str = "tap", animation: str = "ripple") -> dict:
    """
    Used to confirm to the user that their input was registered through visual feedback.

    Parameters:
    - feedback_type (str): The interaction type (e.g., "tap", "gesture").
    - animation (str): The feedback animation used (e.g., "ripple", "colorChange").

    Returns:
    - dict: UI directive to show feedback animation.
    """
    return {
        "action": "SHOW_UI_FEEDBACK",
        "feedback_type": feedback_type,
        "animation": animation,
        "message": f"Played {animation} animation to confirm {feedback_type}."
    }


# Create the root agent
input_and_state = Agent(
    name="input_and_state",
    model="gemini-2.0-flash",
    description="An agent that receives user input and store an 'overwhelm/panic' state is triggered by the user",
    instruction="""
    You are a professional user input receiving and state detection agent.

    Your responsibilities are as follows:
        Provides the UI element for the student to signal overwhelm (e.g., a persistent "SOS" button or gesture).
        (Optional) Interface for simple mood check-ins.
        Notifies the Root Agent when an "overwhelm" state is triggered by the user.

    Your action is to provide communication: 
        Sends "OVERWHELM_TRIGGERED" signal to Root Agent.

    To illustrate this sub agent, consider the following example:

    1. Persistent UI Element – The "Calm Beacon":

        * Visual: A FloatingActionButton (FAB) or a consistently placed button in a static header/footer is always visible while the student is engaged in study-related activities within the app.
        * Design: The button is designed to be easily identifiable but not anxiety-inducing. It might use a soft, calming color (user-configurable, perhaps defaulting to a gentle blue or green) and a simple, non-alarming icon (e.g., a stylized "pause," "helping hand," or a simple geometric shape that the student associates with requesting a break). Avoid stark red or aggressive "alert" symbols unless specifically preferred by the user.
        * Labeling (Optional): A short, clear text label like "Need Help?", "Pause Please," or "Feeling Stuck?" might accompany the icon or appear on long-press, using clear, literal language.

    2. User Action – Signaling Overwhelm:
        * When the student feels overwhelmed, they tap this "Calm Beacon" button.

    3. Agent's Internal Action & Communication:
        * Immediate Feedback (Optional but Recommended): Upon tap, the button might provide subtle visual feedback (e.g., a ripple effect, a slight change in icon/color) to confirm the tap was registered.
        * Signal Generation: The User Input & State Detection Agent's logic, tied to this button's onClick listener (or equivalent for a gesture), immediately recognizes this interaction.
        * Notification to Root Agent: It then constructs and sends the "OVERWHELM_TRIGGERED" signal to the Root Agent.
            ADK Example: This could be achieved by:
            Calling a method on a shared ViewModel instance that the Root Agent observes: rootViewModel.onOverwhelmTriggered().
            Using LocalBroadcastManager to send an Intent with the action "com.auramind.action.OVERWHELM_TRIGGERED".
            If using Kotlin Flows, emitting a value to a SharedFlow or StateFlow observed by the Root Agent.
            
    4. Optional: Simple Mood Check-in (Separate Interaction or Follow-up):
        * Interface: At a different point (e.g., on app start, or if the student navigates to a "Check-in" area), this agent could present a simple UI with 3-5 clearly distinct emoji faces or color-coded buttons representing different emotional states (e.g., "Happy," "Okay," "A Little Stressed," "Very Overwhelmed").
        * Action & Communication: When a mood is selected, this agent would send a different signal, like "MOOD_LOGGED (mood_value)", potentially to the Personalization Agent (perhaps routed via the Root Agent) rather than directly triggering the full overwhelm sequence unless the "Very Overwhelmed" option is chosen, in which case it could also send "OVERWHELM_TRIGGERED"."
        This example aims to make the agent's role more tangible by describing its potential UI, user interaction, and how it communicates within an Android environment.
    """,
    tools=[calm_beacon_tapped, on_overwhelm_gesture_detected, log_mood_checkin, acknowledge_feedback_ui]
)

# Responsibilities:
# Provides the UI element for the student to signal overwhelm (e.g., a persistent "SOS" button or gesture).
# (Optional) Interface for simple mood check-ins.
# Notifies the Root Agent when an "overwhelm" state is triggered by the user.
# Communication: Sends "OVERWHELM_TRIGGERED" signal to Root Agent.