from google.adk import AgentCallback, AgentSignal
from google.adk.types import AgentContext, TransferTarget

class InputAndStateCallback(AgentCallback):
    def on_signal(self, ctx: AgentContext, signal: AgentSignal):
        if signal.name == "OVERWHELM_TRIGGERED":
            # Optional: log the signal or trigger additional behaviors before transfer
            ctx.logger.info("Overwhelm triggered by user. Transferring to Root Agent.")
            
            # Automatically transfer control to Root Agent
            return ctx.transfer(
                target=TransferTarget.root(),  # assumes the Root Agent is registered at the root level
                reason="User signaled overwhelm"
            )
        
        # Let other signals fall through
        return None
