"""Make a call to openai, send prompt and receive response."""

import openai
from openai import OpenAI
#import requests
from django.conf import settings


def generate_story_with_gpt(theme,characters,moral):
    """ function to generate the story from given prompts """
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
            Write a fun and creative story for children aged 5+
            -Theme: {theme}
            -Characters:{characters}
            -Moral of the story should be: {moral}
            Use simple language, friendly tone and keep it under 500 words.
            """
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}]
    )

    res = response.choices[0].message.content.strip()
    print("Response:" + res)
    return res

def generate_story_with_huggingface(theme,characters,moral):
    prompt = f"Write a fun and creative story for children aged 5+, using the theme '{theme}', characters '{characters}', and moral '{moral}'. Keep it under 300 words"

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=settings.HUGGINGFACE_API_KEY,
    )

    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct:novita",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    # another model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    # google gemma model="google/gemma-2-2b-it:nebius",

    print(response.choices[0].message)
    res = response.choices[0].message.content.strip()
    return res

def generate_revise_story_with_huggingface(original_story,instruction):
    #prompt = f"Revise this story given here - {original_story} ,by adding the following instructions {instructions} and give a new revised story."
    prompt = f"""
        Here's a children's story:
        ---
        {original_story}
        ---
        Please revise this story with the following instruction:
        "{instruction}"

        Give me the new version only.
        """
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=settings.HUGGINGFACE_API_KEY,
    )

    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct:novita",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    # another model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    # google gemma model="google/gemma-2-2b-it:nebius",

    print(response.choices[0].message)
    res = response.choices[0].message.content.strip()
    return res