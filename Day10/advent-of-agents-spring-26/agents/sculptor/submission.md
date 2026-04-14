**Note: Make a copy of this for your specific day** 

# Day [X] - Submission

### **Topic: Sculptor Agent (Iterative Pattern)**

### **Owner: [add your ldap]**

### **Status: Started**

### **The Golden Rule: "Always Kata" 🥋**

Our goal is **actionable skills, zero fluff, deployed in under 5 minutes.** If a developer cannot copy-paste your code and see a result in 300 seconds, it is not a Kata.

### **⚠️ The "Lean Team" Reality Check**

We are approaching Google Next. Everyone is busy. We cannot fix broken demos or edit bad videos.

* **The Queue:** We have a prioritized queue. High-quality submissions (perfect code + great video) go live immediately.  
* **The Backlog:** Submissions with "slop" (AI voiceovers, broken snippets, no visuals) go to the back of the line until *you* fix them.

## **📋 The Deliverable Template**

*Please make a copy of this doc and share it with [Owners].*

### **1. The Kata (Website Modal Content)**

*Target Audience: Developers. Style: AdventOfCode / DevRel.*

* **Goal:** Explain *how* it works technically.  
* **Constraint:** 2-3 paragraphs max. No marketing fluff. Pure engineering.  
* **Draft:**  
  When dealing with tasks that require trial and error against an external system (like fixing a compilation error, or finding a specific value in a black-box script), the agent cannot plan everything perfectly upfront. The Sculptor Agent pattern solves this by wrapping an `LlmAgent` in a `LoopAgent`, allowing it to iterate repeatedly until a condition is met.

  The external system is exposed to the agent as a standard `FunctionTool` (e.g., executing a script via `subprocess`). Rather than trying to hard-code validation inside the external system wrapper, we can give the Agent a dedicated `submit_answer` tool. Once the agent is satisfied it has found the answer, it calls this submission tool, which executes `tool_context.actions.escalate = True`, breaking the loop and returning control to the parent process. This creates a self-correcting feedback loop with clear escape hatches and limits (`max_iterations`).

### **2. The Code (The "Modal" Snippet)**

* **Constraint:** Must fit in a code block on a single screen. No massive files.  
* **Type:** CLI Commands or short Python/YAML Snippet.  
* **Requirement:** Must be copy-pasteable and functional.  
* **Snippet:**

```python
import os
import subprocess
from google.adk.tools import ToolContext
from google.adk.agents import LlmAgent, LoopAgent

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
    result = subprocess.run(
        ["python", TARGET_SCRIPT, str(guess)], 
        capture_output=True, text=True
    )
    output = int(result.stdout.strip())
    return {"status": "success", "message": f"Result was {output}."}

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
app = App(name="sculptor", root_agent=root_agent)
```

### **3. Visuals (The "No Slop" Policy) 📹**

*Based on recent feedback, "NotebookLM videos" or generic AI voiceovers feel "sloppy" and will be rejected.*

We need **two** assets:

1. **The "Hype" GIF (Socials):**  
   * **Length:** <20 seconds.  
   * **Content:** Fast-paced screen recording. Terminal flying by, UI updating. Pure dopamine.  
2. **The "Human" Demo (Website):**  
   * **Length:** 3-5 minutes max.  
   * **Content:** A real human (you) talking through the code.  
   * **Tool Tip:** Use **Remotion** or **Vibe Coding** tools to automate the editing, but keep the voice/intent human.

### **4. Links:** 

* [Project Repository](https://github.com/LuisSala/advent-of-agents-spring-26)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [LoopAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
* [Function Tools Reference](https://google.github.io/adk-docs/tools-custom/function-tools/)
