from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from tools.memory_interface import log_to_memory
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
from langchain.chat_models import ChatOpenAI
import json

hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")
llm = HuggingFacePipeline(pipeline=hf_pipeline)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key="your_key_here")


prompt = PromptTemplate(
    input_variables=["json"],  
    template="""
You are a strict JSON validator and normalizer.

TASK:
Given the input JSON payload:
\"\"\"{json_payload}\"\"\"

Perform the following:

1. Extract and normalize the following fields:
    {{
        "id": <string or number>,
        "type": <string>,
        "intent": <string>,
        "status": <string>
    }}

2. If any of these fields are missing in the input, insert the key with the value `"Missing"`.

3. Ensure the output is a valid, well-formatted JSON object with only these 4 keys.

4. Do NOT include any other explanation, note, or extra text. Return only the cleaned JSON.

EXAMPLE OUTPUT:
{{
    "id": "1234",
    "type": "notification",
    "intent": "update",
    "status": "active"
}}
"""
)


chain = LLMChain(llm=llm, prompt=prompt)

def handle_json(filename, conversation_id, content):
    print("Invoked JSONAgent")
    result = chain.invoke({"json_payload":content})
    result = json.dumps(result)

    log_to_memory(
        conversation_id= conversation_id,
        filename=filename,
        format="JSON",
        intent="Unknown",
        extracted_info=result,
        agent="JSONAgent"
    )
    print(f"[JSONAgent] Processed {filename} | Info : {result}")
    