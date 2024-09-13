from dotenv import load_dotenv


load_dotenv(override=True)
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama 
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.query.query_transform import HyDEQueryTransform

from index import load_index
from engines.sub_query import start_engine as start_sub_query_engine
from engines.query import start_engine as start_query_engine
from observability import PheonixWrapper



PheonixWrapper.register_tracer()

# Add llm to global settings
# Settings.llm = Ollama(model="llama3.1")
Settings.llm = OpenAI(model="gpt-3.5-turbo")

index = load_index(input_dir="data", persist_dir="./storage")


# start_sub_query_engine(index)
start_query_engine(index)