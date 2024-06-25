# from crq_app.misc_functions.llm_functions.get_llm_response import get_llm_response

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from misc_functions.llm_functions.get_llm_response import generate_response



def get_response():
    prompt = "What is the best way to learn a new language?"
    response = generate_response(prompt)
    return response

get_response()