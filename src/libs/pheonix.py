
import phoenix as px
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings , set_global_handler

def init_phoenix():
  callback_manager = CallbackManager()
  Settings.callback_manager = callback_manager
  set_global_handler("arize_phoenix")

def launch_app():
  px.launch_app()