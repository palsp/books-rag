from dotenv import load_dotenv

load_dotenv(override=True)
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, load_index_from_storage, StorageContext, set_global_handler
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.core.callbacks import CallbackManager
import phoenix as px
import os


# Add llm to global settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=1024)

# setup observability
# callback_manager = CallbackManager()
# Settings.callback_manager = callback_manager
# px.launch_app()
# set_global_handler("arize_phoenix")



def load_index(input_dir: str, persist_dir: str = "./storage") -> VectorStoreIndex:
  """
  Loads the index from the storage directory. If the storage directory does not exist, it will create the index and store it in the storage directory.
  """
  if not os.path.exists(persist_dir):
    print("Creating storage")
    # load the documents and create the index
    documents = SimpleDirectoryReader(input_dir=input_dir).load_data()
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

index = load_index(input_dir="data", persist_dir="./storage")
chat_engine = index.as_chat_engine(
    chat_mode="react"
)
chat_engine.chat_repl()

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     print("Exiting...")