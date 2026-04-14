**Note: Make a copy of this for your specific day** 

# Day [X] - Submission

### **Topic: Hierarchical Agents (Russian Doll Pattern)**

### **Owner: [add your ldap]**

### **Status: Started**

### **1. The Kata (Website Modal Content)**

*Target Audience: Developers. Style: AdventOfCode / DevRel.*

**The Problem / Why it matters:**

Complex user requests cannot always be decomposed ahead of time. Hardcoding a static sequence of agent steps fails when the prompt requires a dynamically generated plan of attack.

**The Solution:**

The **Hierarchical Agent (Russian Doll)** pattern. We use a top-level Manager agent to orchestrate the flow, leaning on sub-agents to do the heavy lifting.

**How It Works:**

* **AgentTool:** We wrap a "Planner" LLM agent inside an `AgentTool`. The Manager calls this tool at runtime to break the complex problem into smaller, logical steps.

* **Sub-agents block:** The Manager oversees a downstream `SequentialAgent` pipeline (in this case, consisting of a Researcher and Synthesizer).

* **Autonomous Handoff:** Once the Manager receives the generated plan from the Planner tool, it activates the `SequentialAgent` execution pipeline, passing the plan as input so the workers can execute it entirely autonomously without needing a human-in-the-loop.

### **2. The Code (The "Modal" Snippet)**

* **Constraint:** Must fit in a code block on a single screen. No massive files.  
* **Type:** CLI Commands or short Python/YAML Snippet.  
* **Requirement:** Must be copy-pasteable and functional.  
* **Snippet:**

```python
from google.adk.tools import AgentTool
from google.adk.tools import google_search
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App

# The Planner is used purely as a tool by the Manager
planner = LlmAgent(
    name='planner',
    model='gemini-3-flash-preview',
    instruction='Break the user prompt into exactly three distinct research themes.'
)

# Define sub-agents for execution
researcher = LlmAgent(
    name='researcher', 
    model='gemini-3-flash-preview', 
    tools=[google_search], 
    instruction='Research the assigned topic step-by-step.'
)
synthesizer = LlmAgent(
    name='synthesizer', 
    model='gemini-3-flash-preview', 
    instruction='Synthesize the findings into a cohesive report.'
)

# A logical pipeline of sub-agents to handle execution
execution_pipeline = SequentialAgent(
    name='execution_pipeline',
    sub_agents=[researcher, synthesizer]
)

# The Manager orchestrates the whole flow autonomously
manager = LlmAgent(
    name='manager',
    model='gemini-3-flash-preview',
    tools=[AgentTool(planner)],
    sub_agents=[execution_pipeline],
    instruction='''
    1. Use the planner tool to create a detailed research plan based on the user's prompt.
    2. Activate your execution_pipeline sub-agent and pass the completed plan to it so it can execute it.
    '''
)

root_agent = manager
app = App(name="hierarchical", root_agent=root_agent)
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
* [ParallelAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
* [SequentialAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
