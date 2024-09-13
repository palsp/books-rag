import phoenix as px
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings , set_global_handler



class PheonixWrapper:
  @staticmethod
  def register_tracer():
    callback_manager = CallbackManager()
    Settings.callback_manager = callback_manager
    set_global_handler("arize_phoenix")

  @staticmethod
  def launch_app():
    px.launch_app()