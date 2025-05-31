from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from tools.memory_interface import log_to_memory
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
from langchain_community.chat_models import ChatOpenAI
from tools.constants import API_KEY
import json


hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")
llm = HuggingFacePipeline(pipeline=hf_pipeline)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=API_KEY)

prompt = PromptTemplate(
    input_variables=["email"],
    template="""
You are an intelligent, rule-following email processing agent.

TASK:
Read the content of the email provided below and extract ONLY the following items:
1. Sender's email address (look in 'From')
2. Recipient's email address (look in 'To')
3. Intent category: choose exactly one from [complaint, invoice, rfq, regulation, other]
4. Urgency level: choose one from [low, medium, high]

RESPONSE FORMAT:
Sender: <sender_email>
Recipient: <recipient_email>
Intent: <intent>
Urgency: <urgency>

IMPORTANT RULES:
- DO NOT repeat or include the original email content in the response.
- DO NOT add explanations or commentary.
- If any field is missing in the email, write "Unknown" as its value.

EMAIL:
\"\"\"{email}\"\"\"
"""
)


chain = LLMChain(llm=llm, prompt=prompt)

def handle_email(filename, conversation_id, content):
    print("Invoked EmailAgent")
    result = chain.invoke({"email":content})
    result = json.dumps(result)
    log_to_memory(
        conversation_id= conversation_id,
        filename=filename,
        format="Email",
        intent="Unknown",
        extracted_info=result,
        agent="EmailAgent"
    )
    print(f"[EmailAgent] Processed {filename} | Info : {result}")
    