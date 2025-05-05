class Config:
    VECTOR_STORE_PATH = "vector_store.pkl"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    LLM_MODEL = "gemini-1.5-flash"
    MAX_OUTPUT_TOKENS = 1024
    TEMPERATURE = 0.7
    MAX_ITERATIONS = 5
    CHAT_HISTORY_LENGTH = 20