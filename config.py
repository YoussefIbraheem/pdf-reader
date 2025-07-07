from dotenv import load_dotenv
import os 

load_dotenv(override=True, verbose=True)


base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, os.getenv('DATABASE_NAME', 'app.db'))
model_name = os.getenv('MODEL_NAME', 'llama3.2:3b')

class Config:
    # General Config
    SECRET_KEY= os.getenv('SECRET_KEY', 'default_secret_key')
    CHROMA_DATABASE_URL = os.getenv('CHROMA_DATABASE_URL', os.path.join(base_dir, 'db', 'chroma_data'))
    MODEL_NAME= model_name
    CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
    CHROMA_PORT = int(os.getenv('CHROMA_PORT', 8000))