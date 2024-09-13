from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata 
from llama_index.core.query_engine import SubQuestionQueryEngine

def start_engine(index: VectorStoreIndex):
  retriever_engine = index.as_query_engine()
  # Create tools for different aspects of your data
  tools = [
      QueryEngineTool(
          query_engine=retriever_engine,
          metadata=ToolMetadata(
              name="general_retriever",
              description="Useful for answering general questions about the documents"
          )
      ),
      # Add more specialized tools here as needed
  ]

  engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    verbose=True
  )

  while True:
      user_input = input("Enter your question (or 'quit' to exit): ")
      if user_input.lower() == 'quit':
          break
      response = engine.query(user_input)
      print(response)
  
  
  