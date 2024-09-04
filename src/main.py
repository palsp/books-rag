from dotenv import load_dotenv

load_dotenv(override=True)
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, load_index_from_storage, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine
import os

# Add llm to global settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

def load_index(input_files, persist_dir = "./storage") -> VectorStoreIndex:
  """
  Loads the index from the storage directory. If the storage directory does not exist, it will create the index and store it in the storage directory.
  """
  if not os.path.exists(persist_dir):
    print("Creating storage")
    # load the documents and create the index
    documents = SimpleDirectoryReader(input_files=input_files).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=persist_dir)
    return index
  else:
    print("Loading from storage")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index



hyde = HyDEQueryTransform(include_original=True)

sa_index = load_index(input_files=["data/sa_hard_part.pdf"], persist_dir="./storage/sa")
sa_query_engine = sa_index.as_query_engine()
sa_query_engine = TransformQueryEngine(sa_query_engine, hyde)
sa_tool= QueryEngineTool.from_defaults(
  sa_query_engine,
  name="software_architecture",
  description="A specialized query engine for 'Software Architecture: The Hard Parts' by Neal Ford et al. Provides detailed information on advanced software architecture concepts, trade-offs, patterns, and practices discussed in the book. Use for questions about architectural decisions, distributed systems design, and handling complexity in large-scale software systems."
)

agent = ReActAgent.from_tools(
    [sa_tool], verbose=True
)


response = agent.chat(
  "Can you rate horror story saga?"
)
print(response)
