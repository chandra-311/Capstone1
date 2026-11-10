from anthropic import Anthropic
from config.settings import ANTHROPIC_API_KEY, MODEL_NAME

def get_llm_client():
    return Anthropic(api_key=ANTHROPIC_API_KEY)

def get_model_name():
    return MODEL_NAME
