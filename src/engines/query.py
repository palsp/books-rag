from llama_index.core import VectorStoreIndex
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine

def start_engine(index: VectorStoreIndex, use_hyde=True):
  engine = index.as_query_engine()
  if use_hyde:
    hyde = HyDEQueryTransform(include_original=True)
    engine = TransformQueryEngine(engine, hyde)

  while True:
    user_input = input("Enter your question (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    response = engine.query(user_input)
    print(response)
  
  
 
  
  