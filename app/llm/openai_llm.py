from openai import OpenAI
from core.config import settings
from .base_llm import BaseLLM
import numpy as np
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_TEXT_EMBEDDING_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    # def generate_response(self, prompt: str) -> str:
    #     response = self.client.completions.create(
    #         model=self.model,
    #         prompt=prompt,
    #         max_tokens=self.max_tokens,
    #     )
    #     return response.choices[0].text.strip()
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate a response from OpenAI LLM using the given context
        """
        summary = """
        You're an assistant to anser questions using the given context.

        Context: {context}
        
        Answer the following question: {query}
        """
        llm = ChatOpenAI(temperature=self.temperature, model=self.model, api_key=settings.OPENAI_API_KEY)
        prompt_template = PromptTemplate(input_variables=["context"], template=summary)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        result = chain.invoke(input={"context": context, "query": query})
        return result["text"]
    
    def get_embeddings(self, textlist: str) -> str:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=textlist
        )
        embeddings = [data.embedding for data in response.data]
        return np.array(embeddings)
    
openai_llm = OpenAILLM()