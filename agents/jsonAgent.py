from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from tools.memory_interface import log_to_memory
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline

hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")
llm = HuggingFacePipeline(pipeline=hf_pipeline)

prompt = PromptTemplate(
    input_variables=["json"],  
    template="""
You are a JSON validator. Given this JSON input:
"{json_payload}"

1. Normalize the fields into this schema:
    {{
        "id": ...,
        "type": ...,
        "intent": ...,
        "status": ...
    }}

2. Flag if any fields are missing.
3. Return the output as a JSON object.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def handle_json(filename, conversation_id, content):
    result = chain.run(json_payload=content)
    log_to_memory(
        conversation_id= conversation_id,
        filename=filename,
        format="JSON",
        intent="Unknown",
        extracted_info=result,
        agent="JSONAgent"
    )
    print(f"[JSONAgent] Processed {filename} | Info : {result}")
    return result