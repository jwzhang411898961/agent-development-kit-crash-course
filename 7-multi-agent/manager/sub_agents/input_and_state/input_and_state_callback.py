# from google.adk.agents.callback_context import CallbackContext
# from typing import Optional
# from google.genai import types  # For types.Content

# def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
#     for signal in callback_context.step_output.signals:
#         if getattr(signal, "name", "") == "OVERWHELM_TRIGGERED":
#             callback_context.logger.info("OVERWHELM_TRIGGERED detected. Transferring to Root Agent.")
#             # Implement the logic to transfer control to the root agent here.
#             # This might involve setting a flag or modifying the session state.
#             # Since the exact method to transfer control isn't specified in the available documentation,
#             # you may need to consult the latest google.adk documentation or support channels.
#             return None  # Returning None to proceed with default behavior
#     return None  # No action taken if the signal is not detected

# def after_input_agent(ctx: CallbackContext):
#     ctx.logger.info("Input agent finished. Transferring to calm_strategy Agent.")
#     return ctx.transfer("calm_strategy", reason="Input collected, move to calming phase")


# from adk.types import AgentCallbackResult, CallbackContext
# from adk.views import transfer_to_agent



# import logging
# from google.adk.agents.callback_context import CallbackContext

# # Configure the logging system
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # def after_input_agent(ctx: CallbackContext):
# #     ctx.logger.info("Input agent completed. Returning to root.")
# #     return ctx.transfer_to_root(reason="Input complete")


# def after_input_agent(ctx: CallbackContext):
#     # Log the information
#     logger.info("Input agent completed. Returning to root.")
    
#     # Use ctx.transfer to return to the root agent
#     return ctx.transfer("root_agent", reason="Input complete")