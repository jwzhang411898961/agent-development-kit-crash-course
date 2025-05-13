from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import SequentialAgent
from google.adk.tools import google_search

# from .sub_agents.funny_nerd.agent import funny_nerd
# from .sub_agents.news_analyst.agent import news_analyst
# from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.input_and_state.agent import input_and_state
from .sub_agents.study_reengagement.agent import study_reengagement
from .sub_agents.calm_strategy.agent import calm_strategy
from .sub_agents.personalization_and_logging.agent import personalization_and_logging

from .tools.tools import get_current_time

# from google.adk.agents.callback_context import CallbackContext


# def after_root_agent(ctx: CallbackContext):
#     last_agent = ctx.session.step_history[-1].agent_name

#     if last_agent == "input_and_state":
#         return ctx.transfer("calm_strategy", reason="Begin calming")
#     elif last_agent == "calm_strategy":
#         if ctx.session.memory.get("user_is_calm"):
#             return ctx.transfer("study_reengagement", reason="User calmed down")
#         else:
#             return ctx.transfer("calm_strategy", reason="Continue calming")
#     elif last_agent == "study_reengagement":
#         return ctx.transfer("personalization_and_logging", reason="Log session")
#     elif last_agent == "personalization_and_logging":
#         ctx.logger.info("Session complete.")
#         return None

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="The Root/Manager Agent is the central manager of the application, responsible for orchestrating the overall state and user flow—from detecting overwhelm, through calming interventions, to guiding study re-engagement, logging events. It handles primary user interactions (like initiating help), delegates specific tasks to the appropriate Sub-Agents, initiates and terminates their activities, and utilizes user profile data (via the Personalization Agent) to inform its decisions.",
    instruction="""

    Objective: Design a multi-agent framework for an Android application (using ADK) aimed at assisting students with autism spectrum disorder (ASD) in managing emotional dysregulation. The framework should facilitate a calming process when a student feels overwhelmed and gently guide them back to their study tasks. The system will feature a Root Agent coordinating several specialized Sub-Agents.

    Core Problem to Solve: Students with ASD often experience heightened sensory sensitivities and challenges with emotional regulation, leading to overwhelm, meltdowns, or shutdowns, particularly during demanding tasks like studying. This framework aims to provide timely, personalized, and structured support to help them navigate these moments, regain composure, and re-engage with their learning.

    Target Users: Students with Autism Spectrum Disorder (primarily school-aged, but adaptable). (Secondary users: Parents, educators, or therapists for setup and monitoring, though the primary interaction is with the student).

    You are a manager/root agent that is responsible for overseeing the work of the other sub agents. Always delegate the task to the appropriate agent. Use your best judgement to determine which agent to delegate to. Whenever receiving the signal from one sub-agent, immediatelt activate the coresponding next sub-agent.

    Root Agent (Manager Agent):
        Responsibilities:
            Manages the overall application state (e.g., IDLE, STUDYING, OVERWHELMED_DETECTED, CALMING_IN_PROGRESS, REGULATED, RE_ENGAGING).
            Handles primary user interaction for initiating help and navigating main app sections.
            Coordinates and delegates tasks to Sub-Agents based on the received signal, current state and user input.
            Manages user profiles and preferences (links to Personalization Agent data).
            Initiates and terminates Sub-Agent activities.
        Communication: 
            Receives signals from Input/Detection Agent, activates Calming Strategy Agent, then Study Reengagement Agent. Communicates with Personalization & Logging Agent for strategy selection.

    You also have access to the following tools:
        - get_current_time 
  
    """,
    sub_agents=[input_and_state, calm_strategy, study_reengagement, personalization_and_logging],
    tools=[
        # AgentTool(input_and_state),
        get_current_time,
        # google_search
    ], 
    # after_agent_callback=after_root_agent
)

# # Create the sequential agent with minimal callback
# root_agent = SequentialAgent(
#     name="manager",
#     sub_agents=[input_and_state, calm_strategy, study_reengagement, personalization_and_logging],
#     description="The Root/Manager Agent is the central manager of the application, responsible for orchestrating the overall state and user flow—from detecting overwhelm, through calming interventions, to guiding study re-engagement, logging events. It handles primary user interactions (like initiating help), delegates specific tasks to the appropriate Sub-Agents, initiates and terminates their activities, and utilizes user profile data (via the Personalization Agent) to inform its decisions."
# )


    # Sub-Agent 1: User Input & State Detection Agent:
    #     Responsibilities:
    #         Provides the UI element for the student to signal overwhelm (e.g., a persistent "SOS" button or gesture).
    #         (Optional) Interface for simple mood check-ins.
    #         Notifies the Root Agent when an "overwhelm" state is triggered by the user.
    #         Communication: Sends "OVERWHELM_TRIGGERED" signal to Root Agent.
    
    # Sub-Agent 2: Calming Strategy Agent:
    #     Responsibilities:
    #         Manages a library of calming techniques (e.g., breathing exercises, visualizers, audio players, simple interactive activities).
    #         Presents the selected calming strategy/strategies to the user.
    #         Controls the flow of the chosen calming activity (e.g., timers for breathing, sequence of visuals).
    #         Collects feedback on the effectiveness of a strategy post-use (e.g., simple "Did this help?" Yes/No/Maybe).
    #         Communication: Activated by Root Agent. Receives selected strategy information. Sends "CALMING_COMPLETED" or "STRATEGY_EFFECTIVENESS_RATING" to Root Agent and/or Personalization Agent.

    # Sub-Agent 3: Study Reengagement Agent:
    #     Responsibilities:
    #         Offers a structured way to transition back to studying after a calming period.
    #         Presents options like: "Ready to go back?", "Need 5 more minutes?", "Try an easier part of the task?".
    #         Provides positive reinforcement and encouragement.
    #         (Optional) Interface with a simple task list or study timer.
    #         Communication: Activated by Root Agent. Sends "STUDY_RE_ENGAGED" or "NEEDS_FURTHER_BREAK" signals to Root Agent.

    # Sub-Agent 4: Personalization & Logging Agent:
    #     Responsibilities:
    #         Stores and manages user preferences (favorite calming techniques, sensory settings, common triggers if identified).
    #         Logs event data: overwhelm triggers, chosen strategies, duration of calming, user feedback on strategies, re-engagement success.
    #         Analyzes logged data (simple analysis) to suggest more effective strategies over time.
    #         Provides an interface (perhaps for a caregiver) to review logs and adjust preferences.
    #         Communication: Provides data to Root Agent for decision-making. Receives log data from other agents.
