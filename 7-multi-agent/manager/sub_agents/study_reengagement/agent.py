from datetime import datetime
from google.adk.agents import Agent


def present_reengagement_options() -> dict:
    """
    Shows supportive options to the student after a calming activity. 

    Returns:
        dict: UI prompt with re-engagement choices.
    """
    return {
        "event": "SHOW_REENGAGEMENT_PROMPT",
        "prompt": "How are you feeling now?",
        "options": [
            {"id": "ready", "label": "✅ Ready to Study"},
            {"id": "more_time", "label": "🕒 Need 5 More Minutes"},
            {"id": "easier", "label": "📘 Try an Easier Part"}
        ],
        "encouragement": "You're doing great! Just take the next small step."
    }

def handle_reengagement_response(response_id: str) -> dict:
    """
    Interprets the student's response and notifies the Root Agent.

    Parameters:
        response_id (str): One of "ready", "more_time", "easier".

    Returns:
        dict: Signal to the Root Agent based on user's readiness.
    """
    if response_id == "ready":
        return {
            "event": "STUDY_RE_ENGAGED",
            "strategy": "resume_study",
            "timestamp": "auto"
        }
    else:
        return {
            "event": "NEEDS_FURTHER_BREAK",
            "reason": response_id,
            "timestamp": "auto"
        }


# def show_study_timer(duration_minutes: int = 25) -> dict:
#     """
#     Starts a visual study timer to help focus after returning.

#     Parameters:
#     - duration_minutes (int): Duration of the study session in minutes.

#     Returns:
#     - dict: Instructions to show a timer UI.
#     """
#     return {
#         "event": "SHOW_STUDY_TIMER",
#         "duration_minutes": duration_minutes,
#         "message": f"Starting a {duration_minutes}-minute focus session."
#     }

# def show_task_list(tasks: list) -> dict:
#     """
#     Displays a short task list to guide the student after reentry.

#     Parameters:
#     - tasks (list): A list of brief tasks or subtasks.

#     Returns:
#     - dict: Instructions to display a task UI.
#     """
#     return {
#         "event": "SHOW_TASK_LIST",
#         "tasks": tasks,
#         "message": "Here's what you can focus on next."
#     }


# Create the sub agent
study_reengagement = Agent(
    name="study_reengagement",
    model="gemini-2.0-flash",
    description="This sub agent facilitates a smooth and encouraging transition back to study tasks after a student has completed a calming activity.  It presents supportive options for re-engagement, offers positive reinforcement, and communicates the student's readiness (or need for more time) back to the Root Agent.",
    instruction="""
    Study Reengagement Agent:
        When "CALMING_COMPLETED" or "STRATEGY_EFFECTIVENESS_RATING" was sent to Root Agent, this subagent is activated.
        Responsibilities:
            Offers a structured way to transition back to studying after a calming period.
            Presents options like: "Ready to go back?", "Need 5 more minutes?", "Try an easier part of the task?".
            Provides positive reinforcement and encouragement.
            (Optional) Interface with a simple task list or study timer.
        Communication: 
            Activated by Root Agent. Sends "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals to Root Agent.
    """,
    # tools=[present_reengagement_options, handle_reengagement_response, show_study_timer, show_task_list]
    tools=[present_reengagement_options, handle_reengagement_response]
)
