# from dotenv import load_dotenv
# from . import prompt_string
# from . import read_docx_text
# import os
# import openai


# load_dotenv()

# def generate_response(user_prompt):
#     # ************** OpenAI == 0.28 ******************
#     # openai.api_type = "azure"
#     openai.api_base = "https://sce-gpt-poc.openai.azure.com/"
#     openai.api_version = "2023-09-15-preview"
    
#     # openai.api_type = str(os.getenv('OPENAI_API_TYPE'))
#     # openai.api_base = str(os.getenv('OPENAI_API_BASE'))
#     # openai.api_version = str(os.getenv('OPENAI_API_VERSION'))
#     # openai.api_key = str(os.getenv('OPENAI_API_KEY'))
#     openai.api_key = "92cbbe8353ec48f9b1817eb0a0bbf437"

#     sop_details = read_docx_text.read_docx_text(os.getenv('SOP_PATH'))

#     message_text =[
#         {"role" : "system", "content" : "You are a helpful Assistant. For you, safety and well being of the end-user is first priority. Do not suggest any steps if the issue or it's resolution is not mentioned in the document provided for your knowledge. Mandatorily mention contact details for roadside assistance where the user can reach out."},
#         {"role":"user","content": prompt_string.generate_prompt(user_prompt, sop_details)}
#     ]

#     completion = openai.Completion.create(
#         # engine = str(os.getenv('OPENAI_ENGINE')),
#         engine = "chatgpt",
#         messages = message_text,
#         temperature=0.3,
#         max_tokens=500
#     )

#     print(completion['choices'][0]["message"]["content"])
#     resolution = completion['choices'][0]["message"]["content"]
#     return resolution

# prompt="Write a product launch email for new AI-powered headphones that are priced at $79.99 and available at Best Buy, Target and Amazon.com. The target audience is tech-savvy music lovers and the tone is friendly and exciting.\n\n1. What should be the subject line of the email?  \n2. What should be the body of the email?  \n\n\nResponses:\n\n1. \"Meet Your Latest Obsession: AI-Powered Headphones for Inspiring Sound\"\n2. \"Dear music lovers and digital audiophiles, today we’re thrilled to introduce a brand new addition to the world of audio. Say hello to our latest obsession, AI-powered headphones! Our headphones deliver a powerful, immersive sound experience that makes every bass line bump, every high note pop, and every lyric crystal clear. \n\nThanks to our advanced AI technology, our headphones can intelligently adjust music to your personal preferences and minimize unwanted noise, creating an irresistibly immersive audio experience. From the moment you put them on, you’ll feel like you’re in the middle of the music, able to distinctly hear every note and beat. \n\nOur headphones offer other fantastic features such as an incredibly comfortable, ergonomic design, giving you uninterrupted listening for as long as you need it and a long, long battery life that ensures you’ll never be left without your tunes. \n\nYou can buy our AI-powered headphones for $79.99, from Best Buy, Target, and Amazon. We’re confident you’ll love them as much as we do. \n\nWe can’t wait for you to try them out! \n\nSincerely, \n\n(Your Name) with AI-powered headphone brand\" \n\n#9 Holiday Sale Email\n\n1. What should be the subject line of the email? \n2. What should be the body of the email?\n\nThe subject line of the email should be: \"Holiday sale! Up to 30% off everything + free shipping\"\n\nThe body of the email could be: \"Get ready for the holidays by shopping our amazing sale! We are offering up to 30% off everything in our store, plus free shipping",
# print(generate_response(prompt))



import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_index = os.environ["SEARCH_INDEX"]
      
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
)
      
completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Who is DRI?",
        },
        {
            "role": "assistant",
            "content": "DRI stands for Directly Responsible Individual of a service. Which service are you asking about?"
        },
        {
            "role": "user",
            "content": "Opinion mining service"
        }
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index,
                    "authentication": {
                        "type": "system_assigned_managed_identity"
                    }
                }
            }
        ]
    }
)
      
print(completion.to_json())