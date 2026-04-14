# Day [X] - Submission

### **Topic: Writer-Critic Pattern with LoopAgent**

### **Owner: luissala**

### **Status: Complete**

### **1. The Kata (Website Modal Content)**

**The Problem / Why it matters:**

LLMs hallucinate or fail strict formatting rubrics (like word count logic or structural requirements) on the first try. Manually reprompting wastes developer time.

**The Solution:**

The **Writer-Critic (Generator-Evaluator)** pattern. We pit two agents against each other: a creative Writer and a strict Critic who evaluates the draft against a rubric, iterating until perfection.

**How It Works:**

* **LoopAgent:** We wrap the Writer and Critic inside an ADK `LoopAgent`, which automatically cycles execution back-and-forth between its sub-agents up to a `max_iterations` limit.

* **output_key injection:** The Writer saves to `{latest_draft}` and the Critic saves to `{latest_feedback}`. They use these template variables in their prompts to seamlessly read each other's outputs on the next loop cycle.

* **Early Escalation:** The Critic has access to an `approve_draft` function tool. Once the Critic decides the rubric is fully passed, it calls the tool. The tool sets `tool_context.actions.escalate = True`, immediately breaking out of the loop execution early and returning the successful payload.

### **2. The Code (The "Modal" Snippet)**

```python
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool, ToolContext

def approve_draft(tool_context: ToolContext) -> dict:
    tool_context.actions.escalate = True # Breaks the loop execution early
    return {"status": "success", "message": "Approved."}

writer = Agent(
    name='writer', model='gemini-3-flash-preview',
    instruction="Revise your draft based on feedback: {latest_feedback?}",
    output_key='latest_draft'
)

critic = Agent(
    name='critic', model='gemini-3-flash-preview',
    instruction=(
        "Evaluate draft: {latest_draft}. "
        "RUBRIC: 1. Must be sci-fi. 2. Must be under 100 words. "
        "If it FAILS, provide feedback. If it PASSES perfectly, call approve_draft."
    ),
    tools=[FunctionTool(approve_draft)],
    output_key='latest_feedback'
)

root_agent = LoopAgent(name="loop", sub_agents=[writer, critic], max_iterations=4)

from google.adk.apps import App
app = App(name="critic", root_agent=root_agent)
```

**Run it locally:**
```bash
uv run adk run agents/critic
```

### **3. Visuals (The "No Slop" Policy) 📹**

1. **The "Hype" GIF (Socials):**  
   * **Target:** A fast-paced terminal recording of `uv run adk run agents/critic`. Show the Writer failing the word count and missing the required "glitch" keyword, the Critic snapping back with the correction, and the final approved story streaming out.
2. **The "Human" Demo (Website):**  
   * **Target:** A 3-minute screen recording walking through the codebase. Focus heavily on how `output_key` routes the state back into the `{latest_feedback?}` template variable, and how the `escalate=True` tool breaks the ADK loop.

### **4. Links:** 

* [Writer-Critic Demo Source Code](https://github.com/LuisSala/advent-of-agents-spring-26/tree/main/agents/critic)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [LoopAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
* [Function Tools Reference](https://google.github.io/adk-docs/tools-custom/function-tools/)
