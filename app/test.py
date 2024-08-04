from llm.openai_llm import OpenAILLM

if __name__ == "__main__":
    # openai_llm = OpenAILLM()
    # query = "Write code to get a database session"
    # context = "sqlachemy"
    # response = openai_llm.generate_response(query, context)
    # print(response)
    
    openai_embeddings = OpenAILLM()
    textlist = ["This is a test", "This is another test"]
    embeddings = openai_embeddings.get_embeddings(textlist)
    print(embeddings)