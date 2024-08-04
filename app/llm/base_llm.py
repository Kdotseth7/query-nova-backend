class BaseLLM:
    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses should implement this method")
