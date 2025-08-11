"""Make a call to openai, send prompt and receive response."""

import openai
import json
from openai import OpenAI
import requests
from django.conf import settings

def call_hugging_face_api(prompt,model="moonshotai/Kimi-K2-Instruct:novita"):

    # another model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    # google gemma model="google/gemma-2-2b-it:nebius",
    # openai model model="openai/gpt-oss-120b:cerebras",

    for api_key in settings.HUGGINGFACE_API_KEY:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )
        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            if response.status_code ==200:

                print(response.choices[0].message)
                res = response.choices[0].message.content.strip()
                return res
            elif response.status_code == 429:
                print(f"Quota for key :{api_key} exceeded")
                continue
            else:
                response.raise_for_status()

        except Exception as e:
            print(e)
            continue
    raise Exception(f"All API key failed.")
    

# refactoring of below code tobe done.
def generate_story_with_huggingface(theme,characters,moral):
    prompt = f"Write a fun and creative story for children aged 5+, using the theme '{theme}', characters '{characters}', and moral '{moral}'. Keep it under 300 words"

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=settings.HUGGINGFACE_API_KEY[0],
    )
    try:
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct:novita",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        #print("call returned:")
        res = response.choices[0].message.content.strip()
        return res
    except Exception as e:
        raise e
    
def generate_revise_story_with_huggingface(original_story,instruction):

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
        api_key=settings.HUGGINGFACE_API_KEY[0],
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
    
    print(response.choices[0].message)
    res = response.choices[0].message.content.strip()
    return res

def generate_image_prompts_from_story(story_text, num_prompts=3):
    prompt = (
        f"Read the following children's story and write {num_prompts} short prompts for AI-generated images "
        f"that capture the main scenes. Return only a Python list of prompt strings.\n\nStory:\n{story_text}"
    )

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=settings.HUGGINGFACE_API_KEY[0],
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

    try:
        #content = response.model_dump_json()["choices"][0]["message"]["content"]
        res = response.choices[0].message.content.strip()

        # Try parsing the output into a Python list
        prompts = eval(res)
        return prompts if isinstance(prompts, list) else []
    except Exception as e:
        return []
    
    

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