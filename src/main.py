from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(override=True)

from flask import Flask, request, jsonify, abort
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from libs.pheonix import init_phoenix
from data_service import load_index
from llm_service import LLMService

app = Flask(__name__)
Settings.llm = OpenAI(model="gpt-4o")
index = load_index(input_dir="data/design_data_intensive_app", persist_dir="./storage/design_data_intensive_app")
llm_service = LLMService(index, use_sub_query_engine=True)

def initialize_llm_service():
    global llm_service
    index = load_index(input_dir="data/design_data_intensive_app", persist_dir="./storage/design_data_intensive_app")
    llm_service = LLMService(index)

@app.route('/completions', methods=['POST'])
def completions():
    try:
        data = request.get_json()
        if 'message' not in data:
            abort(400, description="No message provided")
    except Exception as e:
        abort(400, description=f"Invalid JSON: {str(e)}")

    message = data['message']

    response = llm_service.get_completion(message)

    # Convert the response to a JSON-serializable format
    response_json = {
        "response": str(response),
    }

    return jsonify(response_json)

if __name__ == '__main__':
  # try:
  #   init_phoenix()
  # except Exception as e:
  #   print("Error starting phoenix", e)

  app.run(debug=True)