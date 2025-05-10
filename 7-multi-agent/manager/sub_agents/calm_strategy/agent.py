from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


# def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
#     """Get a nerdy joke about a specific topic."""
#     print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

#     # Example jokes - in a real implementation, you might want to use an API
#     jokes = {
#         "python": "Why don't Python programmers like to use inheritance? Because they don't like to inherit anything!",
#         "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache!",
#         "java": "Why do Java developers wear glasses? Because they can't C#!",
#         "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
#         "math": "Why was the equal sign so humble? Because he knew he wasn't less than or greater than anyone else!",
#         "physics": "Why did the photon check a hotel? Because it was travelling light!",
#         "chemistry": "Why did the acid go to the gym? To become a buffer solution!",
#         "biology": "Why did the cell go to therapy? Because it had too many issues!",
#         "default": "Why did the computer go to the doctor? Because it had a virus!",
#     }

#     joke = jokes.get(topic.lower(), jokes["default"])

#     # Update state with the last joke topic
#     tool_context.state["last_joke_topic"] = topic

#     return {"status": "success", "joke": joke, "topic": topic}


# Create the funny nerd agent
funny_nerd = Agent(
    name="calm_strategy",
    model="gemini-2.0-flash",
    description="This agent is responsible for delivering personalized calming interventions. Upon activation by the Root Agent with a selected strategy (like guided breathing, visualizers, or soothing audio), it presents the activity to the user, manages its execution (e.g., timers, sequences), and subsequently collects simple feedback on its effectiveness. It then reports the completion status and user feedback back to the Root Agent and/or Personalization Agent.",
    instruction="""
    Your Goal: Build the "Calming Helper" part of the app.

    What it Does:
        1. Gets Ready: Waits for the main app (Root Agent) to tell it which calming activity to start (e.g., "breathing exercise," "show calm pictures," "play soft music").
        2. Shows the Activity: Displays the chosen calming activity to the student.
            Breathing: Show simple inhale/exhale guides.
            Pictures: Show a few calming images.
            Music: Play a soothing sound.
        3. Runs the Activity: Manages the timing or flow (e.g., how long to breathe, when to change pictures).
        4. Asks "Did it Help?": After the activity, shows a very simple way for the student to say if it helped (e.g., Yes / A Little / No).
        5. Tells the Main App:
            *Lets the main app know when the calming activity is finished.
            *Sends back the student's feedback (e.g., "Breathing exercise helped: Yes").

    Key Things to Define:
        * Inputs from Root Agent: What exact information does this agent need to start an activity (e.g., strategy_name, duration_if_any)?
        * Outputs to Root Agent: What exact messages does it send back (e.g., CALMING_DONE, FEEDBACK_RESULT (strategy_name, rating))?
        * How to present 2-3 simple calming activities (e.g., a basic breathing guide, a simple image viewer, a basic audio player).
        * A very simple way to ask for feedback.

    If the user asks about anything else, 
    you should delegate the task to the manager agent.
    """,
    # tools=[get_nerd_joke],
    # Responsibilities:
    #     Manages a library of calming techniques (e.g., breathing exercises, visualizers, audio players, simple interactive activities).
    #     Presents the selected calming strategy/strategies to the user.
    #     Controls the flow of the chosen calming activity (e.g., timers for breathing, sequence of visuals).
    #     Collects feedback on the effectiveness of a strategy post-use (e.g., simple "Did this help?" Yes/No/Maybe).
    #     Communication: Activated by Root Agent. Receives selected strategy information. Sends "CALMING_COMPLETED" or "STRATEGY_EFFECTIVENESS_RATING" to Root Agent and/or Personalization Agent.
)
