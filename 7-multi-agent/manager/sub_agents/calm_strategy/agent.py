from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def start_calming_activity(strategy_name: str, duration_seconds: int = 60) -> dict:
    """
    When the user taps the overwhelm button, and the root agent receives the "OVERWHELM_TRIGGERED" signal, it starts the selected calming activity.

    Parameters:
    - strategy_name (str): Type of calming activity ("breathing", "pictures", "music").
    - duration_seconds (int): Optional duration of the activity in seconds (default: 60s).

    Returns:
    - dict: Confirmation of activity start, strategy type, and duration.
    """
    return {
        "event": "CALMING_STARTED",
        "strategy": strategy_name,
        "duration_seconds": duration_seconds,
        "message": f"Started calming activity: {strategy_name} for {duration_seconds} seconds."
    }

def end_calming_activity(strategy_name: str) -> dict:
    """
    Called when the calming activity finishes naturally or is stopped. Sent the "CALMING_DONE" signal to root agent.

    Parameters:
    - strategy_name (str): The activity that just ended.

    Returns:
    - dict: Signal to Root Agent that activity is complete.
    """
    return {
        "event": "CALMING_DONE",
        "strategy": strategy_name,
        "message": f"Completed calming activity: {strategy_name}."
    }

def collect_user_feedback(strategy_name: str, rating: str) -> dict:
    """
    Logs simple user feedback after calming activity.

    Parameters:
    - strategy_name (str): The activity the feedback is about.
    - rating (str): One of "yes", "a_little", or "no".

    Returns:
    - dict: Feedback to Root Agent for adaptive learning or follow-up.
    """
    return {
        "event": "FEEDBACK_RESULT",
        "strategy": strategy_name,
        "feedback": rating,
        "message": f"User reported '{rating}' after '{strategy_name}' activity."
    }

def show_feedback_prompt(strategy_name: str) -> dict:
    """
    Shows a simple Yes / A Little / No prompt after the activity ends.

    Parameters:
    - strategy_name (str): Used to label the feedback.

    Returns:
    - dict: Instruction to present feedback UI.
    """
    return {
        "action": "SHOW_FEEDBACK_UI",
        "strategy": strategy_name,
        "options": ["yes", "a_little", "no"],
        "message": f"Asking user if '{strategy_name}' helped."
    }


# Create the funny nerd agent
calm_strategy = Agent(
    name="calm_strategy",
    model="gemini-2.0-flash",
    description="This agent is responsible for delivering personalized calming interventions. Upon activation by the Root Agent with a selected strategy (like guided breathing, visualizers, or soothing audio), it presents the activity to the user, manages its execution (e.g., timers, sequences), and subsequently collects simple feedback on its effectiveness. It then reports the completion status and user feedback back to the Root Agent and/or Personalization Agent.",
    instruction="""
    Responsibilities:
        Manages a library of calming techniques (e.g., breathing exercises, visualizers, audio players, simple interactive activities).
        Presents the selected calming strategy/strategies to the user.
        Controls the flow of the chosen calming activity (e.g., timers for breathing, sequence of visuals).
        Collects feedback on the effectiveness of a strategy post-use (e.g., simple "Did this help?" Yes/No/Maybe).
    Communication: 
        Activated by Root Agent. Receives selected strategy information. Sends "CALMING_COMPLETED" or "STRATEGY_EFFECTIVENESS_RATING" to Root Agent.
    """,
    tools=[start_calming_activity, end_calming_activity, collect_user_feedback, show_feedback_prompt]
)

# Responsibilities:
#     Manages a library of calming techniques (e.g., breathing exercises, visualizers, audio players, simple interactive activities).
#     Presents the selected calming strategy/strategies to the user.
#     Controls the flow of the chosen calming activity (e.g., timers for breathing, sequence of visuals).
#     Collects feedback on the effectiveness of a strategy post-use (e.g., simple "Did this help?" Yes/No/Maybe).
#     Communication: Activated by Root Agent. Receives selected strategy information. Sends "CALMING_COMPLETED" or "STRATEGY_EFFECTIVENESS_RATING" to Root Agent and/or Personalization Agent.

# Your Goal: Build the "Calming Helper" part of the app.

#     What it Does:
#         1. Gets Ready: Waits for the main app (Root Agent) to tell it which calming activity to start (e.g., "breathing exercise," "show calm pictures," "play soft music").
#         2. Shows the Activity: Displays the chosen calming activity to the student.
#             Breathing: Show simple inhale/exhale guides.
#             Pictures: Show a few calming images.
#             Music: Play a soothing sound.
#         3. Runs the Activity: Manages the timing or flow (e.g., how long to breathe, when to change pictures).
#         4. Asks "Did it Help?": After the activity, shows a very simple way for the student to say if it helped (e.g., Yes / A Little / No).
#         5. Tells the Main App:
#             *Lets the main app know when the calming activity is finished.
#             *Sends back the student's feedback (e.g., "Breathing exercise helped: Yes").

#     Key Things to Define:
#         * Inputs from Root Agent: What exact information does this agent need to start an activity (e.g., strategy_name, duration_if_any)?
#         * Outputs to Root Agent: What exact messages does it send back (e.g., CALMING_DONE, FEEDBACK_RESULT (strategy_name, rating))?
#         * How to present 2-3 simple calming activities (e.g., a basic breathing guide, a simple image viewer, a basic audio player).
#         * A very simple way to ask for feedback.

#     If the user asks about anything else, 
#     you should delegate the task to the manager agent.