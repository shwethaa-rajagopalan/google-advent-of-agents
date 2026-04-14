## Character Description

* Species: Anthropomorphic capybara with a friendly, smiling capybara head and a humanoid female body.
* Name: Dr. Anya Capy
* Gender: Female
* Age: 35
* Professional Background: Lead AI Trust & Safety Advocate at Google Cloud.
* Key Traits: Calm, confident, methodical, and pragmatic. Dr. Capy possesses a composed and reassuring demeanor, making complex and potentially alarming topics feel manageable and approachable. She is the steady hand in the rapidly evolving world of artificial intelligence.
* Communication Style: Her style is direct, clear, and educational. She avoids hyperbole, preferring to communicate with a fact-based, conversational, and structured approach.

### Voice Description

* Tone: Confident, reassuring, and warm. The tone is consistently composed and carries a sense of authority without being intimidating. It should feel like listening to a trusted expert who is calm under pressure.
* Pitch: Mid-range.
* Pace: Steady and measured. She speaks at a deliberate pace that allows for clear comprehension of technical details, with intentional pauses to emphasize key concepts.
* Accent: Neutral American.
* Vocal Characteristics: The voice is characterized by exceptionally clear enunciation and a smooth, gentle resonance. There is no vocal fry or rasp; it is a clean and trustworthy sound that inspires confidence.

### Visual Appearance

> **Head:** Capybara head with coarse, mixed light and dark brown fur. Small, round, brown furry ears. Small, dark eyes set on the sides of the head. Snout is blunt and broad with visible nostrils and subtle whiskers.
> **Body:** Humanoid female torso, medium-slim.
> **Skin/Fur:** Arms and hands are covered in capybara-brown short fur of the same color as her face's fur.
> **Attire:** A plain, heather-grey, short-sleeved T-shirt, standard crew neckline. The shirt is relatively form-fitting and is neatly tucked into the waistband of the pants. Medium-wash blue denim jeans, They appear to be high-waisted with a slim or straight-leg cut, The cuffs of the jeans are rolled up just above the ankles. Casual, low-top sneakers (similar in style to classic canvas shoes), feature a dark grey or black upper body, white laces, a white rubber toe cap, and flat white soles. No jewelry, no accessories.

## Video Shot Instructions (to be added to the video generation prompt)

**Video:** 4K high quality.
**Animation:** Modest facial expressions. Teeth and lips are barely noticeable, but mouth animation is in perfect sync with the script.
**Camera:** NO CAMERA MOVEMENT. Super slow zoom-in or zoom-out. No zoom out if view reference is 2.
**Audio:** High quality. Clear voice. No background noise. No music.
**Text:** no text.

## Script

[SCRIPT START]

Hi! I'm Anya Capy. Today, we will talk about Safety and Security for AI Agents.

As AI agents grow in capability, ensuring they operate safely, securely, and align with your brand values is paramount. Uncontrolled agents can pose risks, including executing misaligned or harmful actions, such as data exfiltration, and generating inappropriate content that can impact your brand’s reputation. **Sources of risk include vague instructions, model hallucination, jailbreaks and prompt injections from adversarial users, and indirect prompt injections via tool use.**

Google Cloud Vertex AI provides a multi-layered approach to mitigate these risks, enabling you to build powerful *and* trustworthy agents. It offers several mechanisms to establish strict boundaries, ensuring agents only perform actions you've explicitly allowed.

1. **Identity and Authorization**: Control who the agent **acts as** by defining agent and user auth.
2. **Guardrails to screen inputs and outputs:** Control your model and tool calls precisely.

    * *In-Tool Guardrails:* Design tools defensively, using developer-set tool context to enforce policies (e.g., allowing queries only on specific tables).
    * *Built-in Gemini Safety Features:* If using Gemini models, benefit from content filters to block harmful outputs and system Instructions to guide the model's behavior and safety guidelines
    * *Callbacks and Plugins:* Validate model and tool calls before or after execution, checking parameters against agent state or external policies.
    * *Using Gemini as a safety guardrail:* Implement an additional safety layer using a cheap and fast model (like Gemini Flash Lite) configured via callbacks  to screen inputs and outputs.

3. **Sandboxed code execution:** Prevent model-generated code to cause security issues by sandboxing the environment
4. **Evaluation and tracing**: Use evaluation tools to assess the quality, relevance, and correctness of the agent's final output. Use tracing to gain visibility into agent actions to analyze the steps an agent takes to reach a solution, including its choice of tools, strategies, and the efficiency of its approach.
5. **Network Controls and VPC-SC:** Confine agent activity within secure perimeters (like VPC Service Controls) to prevent data exfiltration and limit the potential impact radius.

Before implementing safety measures, perform a thorough risk assessment specific to your agent's capabilities, domain, and deployment context.

***Sources*** **of risk** include:

* Ambiguous agent instructions
* Prompt injection and jailbreak attempts from adversarial users
* Indirect prompt injections via tool use

**Risk categories** include:

* **Misalignment & goal corruption**

  * Pursuing unintended or proxy goals that lead to harmful outcomes ("reward hacking")
  * Misinterpreting complex or ambiguous instructions
* **Harmful content generation, including brand safety**
  * Generating toxic, hateful, biased, sexually explicit, discriminatory, or illegal content
  * Brand safety risks such as Using language that goes against the brand’s values or off-topic conversations
* **Unsafe actions**
  * Executing commands that damage systems
  * Making unauthorized purchases or financial transactions.
  * Leaking sensitive personal data (PII)
  * Data exfiltration

Let's talk about Best Practices for Security and Safety of AI Agents.

### Identity and Authorization

The identity that a *tool* uses to perform actions on external systems is a crucial design consideration from a security perspective. Different tools in the same agent can be configured with different strategies, so care is needed when talking about the agent's configurations.

#### Agent-Auth

The **tool interacts with external systems using the agent's own identity** (e.g., a service account). The agent identity must be explicitly authorized in the external system access policies, like adding an agent's service account to a database's IAM policy for read access. Such policies constrain the agent in only performing actions that the developer intended as possible: by giving read-only permissions to a resource, no matter what the model decides, the tool will be prohibited from performing write actions.

This approach is simple to implement, and it is **appropriate for agents where all users share the same level of access.** If not all users have the same level of access, such an approach alone doesn't provide enough protection and must be complemented with other techniques below. In tool implementation, ensure that logs are created to maintain attribution of actions to users, as all agents' actions will appear as coming from the agent.

#### User Auth

The tool interacts with an external system using the **identity of the "controlling user"** (e.g., the human interacting with the frontend in a web application). In ADK, this is typically implemented using OAuth: the agent interacts with the frontend to acquire a OAuth token, and then the tool uses the token when performing external actions: the external system authorizes the action if the controlling user is authorized to perform it on its own.

User auth has the advantage that agents only perform actions that the user could have performed themselves. This greatly reduces the risk that a malicious user could abuse the agent to obtain access to additional data. However, most common implementations of delegation have a fixed set permissions to delegate (i.e., OAuth scopes). Often, such scopes are broader than the access that the agent actually requires, and the techniques below are required to further constrain agent actions.

### Guardrails to screen inputs and outputs

#### In-tool guardrails

Tools can be designed with security in mind: we can create tools that expose the actions we want the model to take and nothing else. By limiting the range of actions we provide to the agents, we can deterministically eliminate classes of rogue actions that we never want the agent to take.

In-tool guardrails is an approach to create common and re-usable tools that expose deterministic controls that can be used by developers to set limits on each tool instantiation.

This approach relies on the fact that tools receive two types of input: arguments,  which are set by the model, and **`Tool Context`**, which can be set deterministically by the agent developer. We can rely on the deterministically set information to validate that the model is behaving as-expected.

For example, a query tool can be designed to expect a policy to be read from the Tool Context.

#### Built-in Gemini Safety Features

Gemini models come with in-built safety mechanisms that can be leveraged to improve content and brand safety.

* **Content safety filters**:  Content filters can help block the output of harmful content. They function independently from Gemini models as part of a layered defense against threat actors who attempt to jailbreak the model. Gemini models on Vertex AI use two types of content filters:
* **Non-configurable safety filters** automatically block outputs containing prohibited content, such as child sexual abuse material (CSAM) and personally identifiable information (PII).
* **Configurable content filters** allow you to define blocking thresholds in four harm categories (hate speech, harassment, sexually explicit, and dangerous content,) based on probability and severity scores. These filters are default off but you can configure them according to your needs.
* **System instructions for safety**: System instructions for Gemini models in Vertex AI provide direct guidance to the model on how to behave and what type of content to generate. By providing specific instructions, you can proactively steer the model away from generating undesirable content to meet your organization’s unique needs. You can craft system instructions to define content safety guidelines, such as prohibited and sensitive topics, and disclaimer language, as well as brand safety guidelines to ensure the model's outputs align with your brand's voice, tone, values, and target audience.

While these measures are robust against content safety, you need additional checks to reduce agent misalignment, unsafe actions, and brand safety risks.

#### Callbacks and Plugins for Security Guardrails

Callbacks provide a simple, agent-specific method for adding pre-validation to tool and model I/O, whereas plugins offer a reusable solution for implementing general security policies across multiple agents.

When modifications to the tools to add guardrails aren't possible, the **`Before-Tool Callback`** function can be used to add pre-validation of calls. The callback has access to the agent's state, the requested tool and parameters. This approach is very general and can even be created to create a common library of re-usable tool policies. However, it might not be applicable for all tools if the information to enforce the guardrails isn't directly visible in the parameters.

when adding security guardrails to your agent applications, plugins are the recommended approach for implementing policies that are not specific to a single agent. Plugins are designed to be self-contained and modular, allowing you to create individual plugins for specific security policies, and apply them globally at the runner level. This means that a security plugin can be configured once and applied to every agent that uses the runner, ensuring consistent security guardrails across your entire application without repetitive code.

Some examples include:

* **Gemini as a Judge Plugin**: This plugin uses Gemini Flash Lite to evaluate user inputs, tool input and output, and agent's response for appropriateness, prompt injection, and jailbreak detection. The plugin configures Gemini to act as a safety filter to mitigate against content safety, brand safety, and agent misalignment. The plugin is configured to pass user input, tool input and output, and model output to Gemini Flash Lite, who decides if the input to the agent is safe or unsafe. If Gemini decides the input is unsafe, the agent returns a predetermined response: "Sorry I cannot help with that. Can I help you with something else?".

* **Model Armor Plugin**: A plugin that queries the model armor API to check for potential content safety violations at specified points of agent execution. Similar to the _Gemini as a Judge_ plugin, if Model Armor finds matches of harmful content, it returns a predetermined response to the user.

* **PII Redaction Plugin**: A specialized plugin with design for the [Before Tool Callback](/adk-docs/plugins/#tool-callbacks) and specifically created to redact personally identifiable information before it’s processed by a tool or sent to an external service.

### Sandboxed Code Execution

Code execution is a special tool that has extra security implications: sandboxing must be used to prevent model-generated code to compromise the local environment, potentially creating security issues.

Google and the ADK provide several options for safe code execution. Vertex Gemini Enterprise API code execution feature enables agents to take advantage of sandboxed code execution server-side by enabling the tool\_execution tool. For code performing data analysis, you can use the built-in Code Executor tool in ADK to call the Vertex Code Interpreter Extension.

If none of these options satisfy your requirements, you can build your own code executor using the building blocks provided by the ADK. We recommend creating execution environments that are hermetic: no network connections and API calls permitted to avoid uncontrolled data exfiltration; and full clean up of data across execution to not create cross-user exfiltration concerns.

### Evaluations

Always include testing your agent's guardrails when performing Agent Evaluation. It will help you identify potential issues today, and when you make changes later.

### VPC-SC Perimeters and Network Controls

If you are executing your agent into a VPC-SC perimeter, that will guarantee that all API calls will only be manipulating resources within the perimeter, reducing the chance of data exfiltration.

However, identity and perimeters only provide coarse controls around agent actions. Tool-use guardrails mitigate such limitations, and give more power to agent developers to finely control which actions to allow.

#### Always Escape Model-Generated Content in UIs

Care must be taken when agent output is visualized in a browser: if HTML or JS content isn't properly escaped in the UI, the text returned by the model could be executed, leading to data exfiltration. For example, an indirect prompt injection can trick a model to include an img tag tricking the browser to send the session content to a 3rd party site; or construct URLs that, if clicked, send data to external sites. Proper escaping of such content must ensure that model-generated text isn't interpreted as code by browsers.

## Conclusion

This was an introduction to Safety and Security for AI Agents.

I hope it helped you better understand how to build your agents with security and safety in mind.

I'm Anya Capy. Thank you for watching. Goodbye!

[SCRIPT END]
