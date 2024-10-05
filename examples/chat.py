from llama_index.core import VectorStoreIndex

def start_engine(index: VectorStoreIndex):
  chat_engine = index.as_chat_engine()
  chat_engine.chat_repl()
  