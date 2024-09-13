from typing import List, Optional
from dotenv import load_dotenv

load_dotenv(override=True)
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, load_index_from_storage, StorageContext, set_global_handler
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.tools import QueryEngineTool
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
import sys
import os
from logger import Logger


# Add llm to global settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=1024)


logger = Logger("router")


# Check if debug flag is passed
if "--debug" in sys.argv:
    # Using the LlamaDebugHandler to print the trace of the sub questions
    # captured by the SUB_QUESTION callback event type
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager([llama_debug])
else:
    callback_manager = CallbackManager([])  # Default callback manager with no handlers

Settings.callback_manager = callback_manager


def load_index(input_dir: Optional[str] = None, input_files: Optional[List] = None, persist_dir: str = "./storage") -> VectorStoreIndex:
  """
  Loads the index from the storage directory. If the storage directory does not exist, it will create the index and store it in the storage directory.
  """
  if not os.path.exists(persist_dir):
    logger.debug("Creating storage")
    # load the documents and create the index
    documents = SimpleDirectoryReader(input_dir=input_dir, input_files=input_files).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=persist_dir)
    return index
  else:
    logger.debug("Loading from storage")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index

hyde = HyDEQueryTransform(include_original=True)
    
def load_query_engine(index: VectorStoreIndex, hyde: Optional[HyDEQueryTransform] = None) -> RouterQueryEngine:
  engine = index.as_query_engine()
  if hyde:
    engine = TransformQueryEngine(
      index.as_query_engine(),
      hyde
    )
  return engine


def start_engine():
  db_engine = load_query_engine(load_index(input_files=["data/database_internal.pdf"], persist_dir="./storage/database"), hyde=hyde)
  sa_engine = load_query_engine(load_index(input_files=["data/software_architecture.pdf"], persist_dir="./storage/software_architecture"), hyde=hyde)

  db_tool = QueryEngineTool.from_defaults(
      query_engine=db_engine,
      description="A specialized query engine for Database. Provides detailed information on advanced database concepts, trade-offs, patterns, and practices. Use for questions about database design and internal concepts.",
  )
  sa_tool = QueryEngineTool.from_defaults(
      query_engine=sa_engine,
      description="A specialized query engine for Software Architecture. Provides detailed information on advanced software architecture concepts, trade-offs, patterns, and practices. Use for questions about architectural decisions, distributed systems design, and handling complexity in large-scale software systems.",
  )

  engine = RouterQueryEngine(
      selector=PydanticSingleSelector.from_defaults(),
      query_engine_tools=[
        sa_tool,
        db_tool,
      ],
      verbose=True,
  )

  while True:
    user_input = input("Enter your question (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    response = engine.query(user_input)
    print(response)
