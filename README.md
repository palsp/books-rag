# Books RAG Agent

## Project Description

This project operates as a Retrieval-Augmented Generation (RAG) system, specifically crafted to facilitate the querying and extraction of detailed and comprehensive information from a variety of books. It leverages advanced techniques to ensure that users can efficiently retrieve relevant data and insights from the texts.


## Installation Guide

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Steps

1. **Install uv (if not already installed):**

   ```sh
   pip install uv
   ```

2. **Create a virtual environment and install dependencies:**

   ```sh
   uv sync
   ```

3. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the project:**

   ```sh
   uv run src/main.py
   ```

### Usage

After running the project, the agent will be initialized with tools for querying the specified books. You can interact with the agent through the console.
