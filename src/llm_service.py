from llama_index.core import VectorStoreIndex
from query_engine import create_sub_query_engine, create_query_engine


class LLMService:
  def __init__(self, index: VectorStoreIndex, use_sub_query_engine: bool = False):
    self.index = index

    if use_sub_query_engine == "sub":
      self.engine = create_sub_query_engine(self.index)
    else:
      self.engine = create_query_engine(self.index, use_hyde=False)

    
  def get_completion(self, message: str):
    response = self.engine.query(message)
    return response
  
  