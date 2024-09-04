from dotenv import load_dotenv

load_dotenv(override=True)
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, load_index_from_storage, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
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



index = load_index(input_files=["data/sa_hard_part.pdf"], persist_dir="./storage/sa")
software_architecture_tool= QueryEngineTool.from_defaults(
  index.as_query_engine(),
  name="software_architecture",
  description="A specialized query engine for 'Software Architecture: The Hard Parts' by Neal Ford et al. Provides detailed information on advanced software architecture concepts, trade-offs, patterns, and practices discussed in the book. Use for questions about architectural decisions, distributed systems design, and handling complexity in large-scale software systems."
)


index = load_index(input_files=["data/implementing_ddd.pdf"], persist_dir="./storage/ddd")
ddd_tool= QueryEngineTool.from_defaults(
  index.as_query_engine(),
  name="domain_driven_design",
  description="A specialized query engine for 'Implementing Domain-Driven Design' by Vaughn Vernon. Provides detailed information on domain-driven design concepts, patterns, and practices discussed in the book. Use for questions about domain modeling, bounded contexts, and event sourcing."
)

agent = ReActAgent.from_tools(
    [software_architecture_tool, ddd_tool], verbose=True
)


response = agent.chat(
  "Can you rate Horror Story saga?"
)
print(response)