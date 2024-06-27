# -*- coding: utf-8 -*-
"""PoC-Solar Farm

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VnylzolMFh89XCq4fh8V2HTO8LeeOPSb
"""

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

img = Image.open("/content/D1-Solar Panel.jpg").convert('RGB')

text = "a photography of"
inputs = processor(img, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

user_input=processor.decode(out[0], skip_special_tokens=True)

pip install python-docx

from docx import Document

def read_docx_text(filepath):
  """Reads text from a .docx file and stores it in a variable.

  Args:
    filepath: Path to the .docx file.

  Returns:
    Extracted text as a string.
  """
  doc = Document(filepath)
  all_paragraphs = ""
  for paragraph in doc.paragraphs:
    all_paragraphs += paragraph.text + "\n"
  return all_paragraphs

# Example usage
SOP = read_docx_text("/content/Broken Window Manual.docx")
print(SOP)

pip install openai

import openai

from openai import AzureOpenAI

api_type = "azure"
api_base = "https://sce-gpt-poc.openai.azure.com/"
api_version = "2023-09-15-preview"
api_key = "92cbbe8353ec48f9b1817eb0a0bbf437"
deployment_name = 'chatgpt'

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)

response = client.completions.create(
    model=deployment_name,
    prompt="""You are an expert staff who 9knows how to do repair and maintenance of so;ar panels.

    Step 1: Understand whether or not there are objects detected on a solar panel from {ui}
    Step 2: Suggest the right course of action to mitigate the risk

    Strictly follow the below instructions while giving your answer:
    1. Please Mention only the steps that shpold be taken and not anything else.
    2. Give step by step instructions and only in plain text format
    3. After mentioning the steps, do not mention anything else

    """.format(ui="a photography of a red glove on the ground next to a solar panel"),
    max_tokens=150
)
print(response.choices[0].text)
text = response.choices[0].text

# Install the deep_translator module
!pip install deep_translator

# Import the necessary modules
from deep_translator import GoogleTranslator

# Create a translator object
translator = GoogleTranslator(source='auto', target='hi')

# Define a function to translate text to Hindi
def translate_to_hindi(text):
  translation = translator.translate(text)
  return translation

# Get the input text from the user
input_text = text

# Translate the input text to Hindi
translated_text = translate_to_hindi(input_text)

# Print the translated text
print(translated_text)

pip install azure-cognitiveservices-speech

pip install python-dotenv

# Commented out IPython magic to ensure Python compatibility.
# %%writefile .env
# # Add your environment variables here
# SPEECH_KEY = 4806bf3bda8e4248b8bf0a3a4be767f7
# SPEECH_REGION = eastus

!ls -la

pip install --upgrade azure-cognitiveservices-speech

import os
import azure.cognitiveservices.speech as speechsdk

speech_key, service_region,endpoint = "4806bf3bda8e4248b8bf0a3a4be767f7", "eastus","https://eastus.api.cognitive.microsoft.com/"

speech_config = speechsdk.SpeechConfig(subscription=speech_key,endpoint=endpoint)

speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

print("Type some text that you want to speak...")
text = input()


result = speech_synthesizer.speak_text_async(text).get()


if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized to speaker for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
    print("Did you update the subscription info?")