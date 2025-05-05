from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from config import Config
from tools import (
    wikipedia_tool,
    study_tips_tool,
    google_search_tool,
    youtube_summary_tool,
    exam_strategy_tool,
    flashcard_generator_tool,
    note_organizer_tool,
    concept_mapper_tool,
    scholarly_papers_tool,
    subject_expert_tool
)

def run_agent(query: str):
    llm = ChatGoogleGenerativeAI(
        model=Config.LLM_MODEL,
        temperature=Config.TEMPERATURE,
        max_output_tokens=Config.MAX_OUTPUT_TOKENS,
        convert_system_message_to_human=True  
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    tools = [
        Tool(
            name="Wikipedia Tool",
            func=wikipedia_tool,
            description="Fetch Wikipedia summaries on academic topics, concepts, and theories."
        ),
        Tool(
            name="Study Tips Tool", 
            func=study_tips_tool, 
            description="Provide personalized study tips for different subjects and learning styles."
        ),
        Tool(
            name="Google Search Tool", 
            func=google_search_tool, 
            description="Search Google for recent academic information and facts."
        ),
        Tool(
            name="YouTube Summary Tool", 
            func=youtube_summary_tool, 
            description="Summarize educational YouTube videos. Input: YouTube Video ID or URL."
        ),
        Tool(
            name="Exam Strategy Tool", 
            func=exam_strategy_tool, 
            description="Get specific tips for different exam formats: MCQ, theory, practical, or viva."
        ),
        Tool(
            name="Flashcard Generator Tool", 
            func=flashcard_generator_tool, 
            description="Generate study flashcards for any topic with question-answer pairs."
        ),
        Tool(
            name="Note Organizer Tool", 
            func=note_organizer_tool, 
            description="Organize and structure study notes for better comprehension."
        ),
        Tool(
            name="Concept Mapper Tool", 
            func=concept_mapper_tool, 
            description="Create concept maps showing relationships between ideas for visual learning."
        ),
        Tool(
            name="Scholarly Papers Tool", 
            func=scholarly_papers_tool, 
            description="Find and summarize academic papers on a given topic."
        ),
        Tool(
            name="Subject Expert Tool", 
            func=subject_expert_tool, 
            description="Get specialized help from virtual subject matter experts in various fields."
        ),
    ]

    class ToolTracker:
        def __init__(self):
            self.tools_used = set()
        
        def track_tool_usage(self, tool_name):
            self.tools_used.add(tool_name)

    tool_tracker = ToolTracker()
    
    def _track_tool_usage(tool_name):
        tool_tracker.track_tool_usage(tool_name)
    
    for tool in tools:
        original_func = tool.func
        tool.func = lambda query, tool_name=tool.name, func=original_func: (_track_tool_usage(tool_name), func(query))[1]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        max_iterations=Config.MAX_ITERATIONS,
        early_stopping_method="generate",
    )
    
    try:
        response = agent.run(f"Based on all available information, please provide a detailed and helpful answer to this query: {query}")
        return response, list(tool_tracker.tools_used)
    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try rephrasing your question.", list(tool_tracker.tools_used)