import os
import subprocess
import sys
import asyncio
from typing import AsyncGenerator

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import ToolContext, FunctionTool

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_SCRIPT = os.path.join(SCRIPT_DIR, "target_script.py")

# ==============================================================================
# NOTES: OPAQUE SYSTEM INTERACTION
# ==============================================================================
# In this agent, we simulate interacting with an opaque external system.
# We define a function `validate_guess` that interacts with a Python script via
# `subprocess` and returns the resulting value. This serves as our feedback loop.
# ==============================================================================
def validate_guess(guess: int) -> dict:
    """Passes a guess to the opaque external system. Returns the resulting value."""
    try:
        # Execute out-of-process
        result = subprocess.run(
            [sys.executable, TARGET_SCRIPT, str(guess)],
            capture_output=True, text=True, check=True
        )
        output_y = int(result.stdout.strip())
        
        # Feedback for the next iteration
        return {"status": "success", "message": f"Result was {output_y}."}
    except Exception as e:
         return {"status": "error", "message": f"Script failed: {e}"}

# ==============================================================================
# NOTES: LOOP ESCALATION
# ==============================================================================
# We also provide an `exit_loop` tool. When the agent is satisfied it has
# found the correct answer, it executes this function. We then set
# `tool_context.actions.escalate = True` which triggers the parent LoopAgent
# to terminate immediately, effectively breaking the loop.
# ==============================================================================
def exit_loop(tool_context: ToolContext) -> dict:
    """Call this tool to stop iterating once you found the correct value."""
    tool_context.actions.escalate = True
    return {"status": "success"}

# ==============================================================================
# NOTES: LLM GUESSER
# ==============================================================================
# The LlmAgent is given instructions to guess a value, observe the result,
# and dynamically adjust its next guess until it successfully hits the target.
# ==============================================================================
sculptor = LlmAgent(
    name="sculptor",
    model="gemini-3-flash-preview",
    instruction="""
    Find the input 'x' that yields the integer provided by the user. 
    If the user does not provide a number, then use '17' as your target number. 
    You will be executing in a loop until you find the correct answer.
    Use validate_guess to test, and exit_loop to exit the loop once you find the answer.
    Please output your guesses to the user on every iteration.
    """,
    tools=[validate_guess, exit_loop]
)

# ==============================================================================
# NOTES: LOOP AGENT
# ==============================================================================
# The LoopAgent wraps our LlmAgent. It will repeatedly invoke the sub-agent
# until it either escalates (via exit_loop) or reaches max_iterations.
# ==============================================================================
root_agent = LoopAgent(
    name="iterator_loop",
    sub_agents=[sculptor],
    max_iterations=10
)

from google.adk.apps import App

app = App(
    name="sculptor",
    root_agent=root_agent
)

if __name__ == '__main__':
    # Provided for local testing if running directly with `uv run python` instead of `adk run`
    import asyncio
    from google.adk.runners import InMemoryRunner

    async def run_demo():
        runner = InMemoryRunner(app=app)
        print("Starting Sculptor Demo (Looping over Opaque Target)...")
        await runner.run_debug("The target number is 23. Find the 'x' that gets this output.")

    asyncio.run(run_demo())
