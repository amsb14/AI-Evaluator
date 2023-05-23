import joblib
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
loaded_model = joblib.load('GaiaPropertyPredictor2.pkl')