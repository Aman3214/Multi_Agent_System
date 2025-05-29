from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from tools.memory_interface import log_to_memory
from langchain.llms import huggingface_pipeline
from transformers import pipeline

hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")
llm = huggingface_pipeline(pipeline=hf_pipeline)

prompt = PromptTemplate(
    input_variables=["email"],  
    template="""
You are an intelligent email processor. Given this mail content:
"{email}"

Extract:
- Sender (if present)
- Recipient (if present)
- Intent (complaint, invoice, rfq, regulation, other)
- Urgency (low, medium, high)
Return a JSON object with the extracted fields.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def handle_email(filename, conversation_id, content):
    result = chain.run(email=content)
    log_to_memory(
        conversation_id= conversation_id,
        filename=filename,
        format="Email",
        intent="Unknown",
        extracted_info=result,
        agent="EmailAgent"
    )
    print(f"[EmailAgent] Processed {filename} | Info : {result}")
    return result