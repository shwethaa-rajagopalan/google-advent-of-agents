# Day [X] - Submission

### **Topic: Parallel LLM Fanout and State Interpolation**

### **Owner: luissala**

### **Status: Draft**

### **1. The Kata (Website Modal Content)**

*Target Audience: Developers. Style: AdventOfCode / DevRel.*

**The Problem / Why it matters:**

Sequential LLM calls are painfully slow. In multi-agent systems involving independent tasks (like running multiple research queries), executing them one by one creates unacceptable latency.

**The Solution:**

The ADK **Parallel Fanout** pattern. We can spin up multiple independent agents to run concurrently, and automatically synthesize their results together when they finish.

**How It Works:**

* **ParallelAgent:** Groups independent feature agents together so they are executed simultaneously, dramatically cutting down wall-clock execution time.

* **output_key:** Assigning an `output_key` to each parallel worker allows ADK to implicitly save their return payload directly into the session State.

* **State Interpolation:** A downstream `SequentialAgent` handles the synthesis step. Because the parallel workers populated the state dictionary, we simply use `{bracket}` templating (e.g., `{healthcare_research}`) in our synthesizer's instruction prompt—no custom data-passing code required.

### **2. The Code (The "Modal" Snippet)**

* **Constraint:** Must fit in a code block on a single screen. No massive files.  
* **Type:** CLI Commands or short Python/YAML Snippet.  
* **Requirement:** Must be copy-pasteable and functional.  
* **Snippet:**

```python
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Define independent research agents with explicit output_keys and grounding tools
healthcare_researcher = Agent(name='healthcare_researcher', model='gemini-3-flash-preview', output_key='healthcare_research', tools=[google_search], instruction='Use the Google Search tool to...')
finance_researcher = Agent(name='finance_researcher', model='gemini-3-flash-preview', output_key='finance_research', tools=[google_search], instruction='Use the Google Search tool to...')

# 2. Fanout: Run them all concurrently
research_squad = ParallelAgent(
    name='research_squad',
    sub_agents=[healthcare_researcher, finance_researcher],
)

# 3. State Interpolation: Use `{output_key}` placeholders in the synthesizer prompt
synthesizer = Agent(
    name='synthesizer',
    model='gemini-3-flash-preview',
    instruction="Synthesize the following trends: \n\n{healthcare_research}\n\n{finance_research}",
)

# 4. Sequential block ensures fanout completes and populates state before synthesis
root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[research_squad, synthesizer],
)

from google.adk.apps import App
app = App(name="fanout", root_agent=root_agent)
```

### **3. Visuals (The "No Slop" Policy) 📹**

*Based on recent feedback, "NotebookLM videos" or generic AI voiceovers feel "sloppy" and will be rejected.*

We need **two** assets:

1. **The "Hype" GIF (Socials):**  
   * **Length:** <20 seconds.  
   * **Content:** Fast-paced screen recording showing multiple researcher logs executing concurrently and resolving to a final report.
2. **The "Human" Demo (Website):**  
   * **Length:** 3-5 minutes max.  
   * **Content:** Real human talking through how `output_key` implicitly solves data routing issues when chaining complex agents in ADK.

### **4. Links:** 

* [Project Repository](https://github.com/LuisSala/advent-of-agents-spring-26)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [ParallelAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
* [SequentialAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)