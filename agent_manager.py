from langchain.agents import initialize_agent, Tool
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
from agents.emailAgent import handle_email
from agents.jsonAgent import handle_json 

hf_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
llm = HuggingFacePipeline(pipeline=hf_pipeline)

tools = [
    Tool(
        name="handle_email",
        func=lambda x: handle_email(**x),
        description="Handles emails and extracts information",
    ),
    Tool(
        name="handle_json",
        func=lambda x: handle_json(**x),
        description="Handle json and reformats if needed",
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)