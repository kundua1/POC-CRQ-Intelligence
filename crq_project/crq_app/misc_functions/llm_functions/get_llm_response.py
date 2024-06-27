from dotenv import load_dotenv
from read_docx_text import read_docx_text
from prompt_string import system_prompt, user_prompt
import os
import openai

load_dotenv()


def generate_llm_response(project_name, dependent_applications):
    environment = str(os.getenv('OPENAI_SUBSCRIPTION'))
    if environment == "Dev":
        # ************** OpenAI == 0.28 ******************
        openai.api_type = os.getenv('API_TYPE')
        openai.api_base = os.getenv('API_BASE')
        openai.api_version = os.getenv('API_VERSION')
        openai.api_key = os.getenv('API_KEY')
        deployment_name = os.getenv('DEPLOYMENT_NAME')

        sop_details = read_docx_text(os.getenv('SOP_PATH'))

        message_text =[
            {"role" : "system", "content" : system_prompt(sop_details)},
            {"role":"user", "content": user_prompt(project_name, dependent_applications)}
        ]

        completion = openai.ChatCompletion.create(
            engine = deployment_name,
            messages = message_text,
            temperature=0.3,
            max_tokens=500
        )

        print(completion['choices'][0]["message"]["content"])
        resolution = completion['choices'][0]["message"]["content"]
        return resolution
    
    elif environment == "Innovation":
        # ************** OpenAI == 0.28 ******************
        openai.api_type = os.getenv('OPENAI_API_TYPE')
        openai.api_base = os.getenv('OPENAI_API_BASE')
        openai.api_version = os.getenv('OPENAI_API_VERSION')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        deployment_name = os.getenv('OPENAI_DEPLOYMENT_NAME')

        sop_details = read_docx_text(os.getenv('SOP_PATH'))

        message_text =[
            {"role" : "system", "content" : system_prompt(sop_details)},
            {"role":"user", "content": user_prompt(project_name, dependent_applications)}
        ]

        completion = openai.ChatCompletion.create(
            engine = deployment_name,
            messages = message_text,
            temperature=0.3,
            max_tokens=500
        )

        print(completion['choices'][0]["message"]["content"])
        resolution = completion['choices'][0]["message"]["content"]
        return resolution


project_name = ""
dependent_applications = ""
ans = generate_llm_response(project_name=project_name, dependent_applications=dependent_applications)
print(ans)
