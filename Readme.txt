# AI Study Assistant

An intelligent educational companion powered by Google's Gemini model and LangChain that provides personalized academic support through conversational AI.

## Features

- Natural language chat interface built with Streamlit
- Intelligent agent system using LangChain and Google Gemini
- 10 specialized educational tools:
  - Wikipedia Tool
  - Study Tips Tool
  - Google Search Tool
  - YouTube Summary Tool
  - Exam Strategy Tool
  - Flashcard Generator Tool
  - Note Organizer Tool
  - Concept Mapper Tool
  - Scholarly Papers Tool
  - Subject Expert Tool
- Tool usage tracking and transparency
- Conversation memory for contextual interactions

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-study-assistant.git
   cd ai-study-assistant
   ```

2. Install the required packages:
   ```
   pip install streamlit langchain langchain_google_genai python-dotenv youtube_transcript_api wikipedia requests
   ```

3. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   MODEL_NAME=gemini-1.5-flash
   VECTOR_STORE_PATH=vector_store.pkl
   EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
   SERPAPI_API_KEY=your_serpapi_key
   ```

## Usage

1. Start the application:
   ```
   streamlit run main.py
   ```

2. Access the web interface at http://localhost:8501

3. Type your study-related questions in the chat box

4. View responses and which tools were used to answer your question

## Project Structure

- `main.py`: Streamlit web interface
- `agent.py`: LangChain agent implementation
- `tools.py`: Educational tools collection
- `config.py`: Configuration settings
- `.env`: Environment variables and API keys

## Requirements

- Python 3.8+
- Google API key (for Gemini access)
- SerpAPI key (for search tools)
- Internet connection for external API access

## License

MIT

## Acknowledgments

- LangChain for the agent framework
- Google for the Gemini model
- Streamlit for the web interface