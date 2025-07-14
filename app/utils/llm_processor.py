from langchain_ollama import ChatOllama
from app import config

class LLMProcessor:
    def __init__(self, model_name=config.MODEL_NAME):
        self.model_name = model_name

    def get_llm(self):
        return ChatOllama(model=self.model_name)