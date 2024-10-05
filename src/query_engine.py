from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata 
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core import VectorStoreIndex
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine

def create_sub_query_engine(index: VectorStoreIndex):
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

  return engine


def create_query_engine(index: VectorStoreIndex, use_hyde=True):
  engine = index.as_query_engine()
  if use_hyde:
    hyde = HyDEQueryTransform(include_original=True)
    engine = TransformQueryEngine(engine, hyde)

  return engine


  
 
  
  