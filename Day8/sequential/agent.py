from google.adk.agents import LlmAgent, SequentialAgent

# Step 1: The Reader - Ingests the PDF and normalizes the content
reader = LlmAgent(
   model='gemini-3.1-pro-preview',
   name="PDFReader",
   instruction="Analyze the provided PDF and provide a comprehensive raw text dump of its core contents.",
   output_key="parsed_content"
)

# Step 2: The Insight Miner - Identifies key technical facts or unique points
miner = LlmAgent(
   model='gemini-3.1-pro-preview',
   name="InsightMiner",
   instruction="""
   Review the following content: {parsed_content}
   Extract the top 5 most important technical facts, dates, or figures.
   """,
   output_key="extracted_insights"
)

# Step 3: The Synthesizer - Generates the final "TL;DR"
synthesizer = LlmAgent(
   model='gemini-3.1-pro-preview',
   name="ExecutiveSynthesizer",
   instruction="""
   Based on these insights: {extracted_insights}
   Generate a 3-sentence 'Executive Briefing' suitable for a busy stakeholder.
   """
)

# Orchestrate the linear Assembly Line
root_agent = SequentialAgent(
   name="UniversalDocumentPipeline",
   sub_agents=[reader, miner, synthesizer]
)