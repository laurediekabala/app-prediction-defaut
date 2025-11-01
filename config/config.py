import os

class Config:
    # Flask API settings
    FLASK_HOST = os.getenv('FLASK_HOST', 'http://127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Streamlit settings
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))
    
    @classmethod
    def get_api_url(cls):
        return f"{cls.FLASK_HOST}:{cls.FLASK_PORT}"