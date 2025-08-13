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
    print("Callin hugging face api")
    last_error = ""
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
            print(e) #logging
            last_error = str(e)
            continue
    raise Exception(f"All API key failed. Last error: {last_error}")
    
def generate_story_with_huggingface(theme,characters,moral):
    prompt = f"Write a fun and creative story for children aged 5+, using the theme '{theme}', characters '{characters}', and moral '{moral}'. Keep it under 300 words"

    try:
        res = call_hugging_face_api(prompt=prompt)
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
    try:
        res = call_hugging_face_api(prompt=prompt)
    except Exception as e:
        raise e

def generate_image_prompts_from_story(story_text, num_prompts=3):
    prompt = (
        f"Read the following children's story and write {num_prompts} short prompts for AI-generated images "
        f"that capture the main scenes. Return only a Python list of prompt strings.\n\nStory:\n{story_text}"
    )

    try:
        #content = response.model_dump_json()["choices"][0]["message"]["content"]
        #res = response.choices[0].message.content.strip()
        res = call_hugging_face_api(prompt=prompt)

        # Try parsing the output into a Python list
        prompts = eval(res)
        return prompts if isinstance(prompts, list) else []
    except Exception as e:
        return []
    
    
def generate_worksheet_content(subject, grade, worksheet_type, topic, num_questions=10):
    prompt = f"""
    You are an educational content generator.
    Generate {num_questions} {worksheet_type} questions for {subject} for Grade {grade}
    on the topic "{topic}". Provide answers separately.
    Format output as JSON with "questions" and "answers".
    """

    try:
        """response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an educational content generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message["content"]"""
        res = call_hugging_face_api(prompt=prompt)
        return res
    except Exception as e:
        return {"error": str(e)}


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