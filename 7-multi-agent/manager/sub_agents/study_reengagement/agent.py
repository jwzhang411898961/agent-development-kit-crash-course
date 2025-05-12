from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent


def prompt_study_reengagement(current_task: str = "") -> dict:
    """
    Prompts the student with reengagement options after a calming break.

    Parameters:
    - current_task (str): Optional description of the task the student was working on.

    Returns:
    - dict: Contains message and options to present in the UI.
    """
    return {
        "event": "SHOW_REENGAGEMENT_PROMPT",
        "message": "Would you like to get back to your task?",
        "task": current_task,
        "options": [
            {"id": "ready_to_return", "label": "I'm ready!"},
            {"id": "need_more_time", "label": "Need 5 more minutes"},
            {"id": "try_easier_part", "label": "Can I try an easier part?"}
        ]
    }

def handle_reengagement_response(response: str) -> dict:
    """
    Handles the student's selection from the reengagement prompt.

    Parameters:
    - response (str): One of 'ready_to_return', 'need_more_time', 'try_easier_part'

    Returns:
    - dict: Signal to send back to the Root Agent.
    """
    if response == "ready_to_return":
        return {
            "event": "STUDY_RE_ENGAGED",
            "message": "Student is ready to return to study."
        }
    else:
        return {
            "event": "NEEDS_FURTHER_BREAK",
            "reason": response,
            "message": f"Student chose: {response.replace('_', ' ')}."
        }

def show_study_timer(duration_minutes: int = 25) -> dict:
    """
    Starts a visual study timer to help focus after returning.

    Parameters:
    - duration_minutes (int): Duration of the study session in minutes.

    Returns:
    - dict: Instructions to show a timer UI.
    """
    return {
        "event": "SHOW_STUDY_TIMER",
        "duration_minutes": duration_minutes,
        "message": f"Starting a {duration_minutes}-minute focus session."
    }

def show_task_list(tasks: list) -> dict:
    """
    Displays a short task list to guide the student after reentry.

    Parameters:
    - tasks (list): A list of brief tasks or subtasks.

    Returns:
    - dict: Instructions to display a task UI.
    """
    return {
        "event": "SHOW_TASK_LIST",
        "tasks": tasks,
        "message": "Here's what you can focus on next."
    }


# Create the sub agent
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
    tools=[prompt_study_reengagement, handle_reengagement_response, show_study_timer, show_task_list]
)
