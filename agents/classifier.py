from transformers import pipeline
from tools.constants import INTENT_LABELS, FORMAT_LABELS
from tools.memory_interface import log_to_memory
from agents.emailAgent import handle_email
from agents.jsonAgent import handle_json
# from agent_manager import agent
# import json

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_format(content, filename):
    ext = filename.split(".")[-1].lower()
    if ext == "txt":
        return "Email"
    elif ext == "json":
        return "JSON"
    elif ext == "pdf":
        return "PDF"
    else:
        format_result = classifier(content, FORMAT_LABELS)
        return format_result["labels"][0]
def classify_input(filename,conversation_id, content):
    intent_result = classifier(content, INTENT_LABELS)
    intent = intent_result["labels"][0]

    format_ = detect_format(content, filename)

    log_to_memory(
        conversation_id= conversation_id,
        filename=filename,
        format=format_,
        intent=intent,
        extracted_info="{}",
        agent="Classifier"
    )
    
    input_payload = {
        "filename": filename,
        "conversation_id": conversation_id,
        "content": content
    }
    print(f"[Classifier] Processed {filename} | Intent: {intent} | Format: {format_}")

       
    if format_ == "Email":
        print("[Classifier] Invoking EmailAgent")
        handle_email(**input_payload)
    elif format_ == "JSON":
        print("[Classifier] Invoking JSONAgent")
        handle_json(**input_payload)
    else:
        print("Unsupported format")
    
    return {
        "intent": intent,
        "format": format_
    }
