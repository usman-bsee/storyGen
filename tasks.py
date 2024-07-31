from celery_config import app
import requests

IP_ADDRESS = "127.0.0.1"
URL = f"http://{IP_ADDRESS}:5100"


@app.task(name='tasks.process_story2description')
def process_story2description(json_data):
    s2d_url = f"{URL}/process_story2description"
    response = requests.post(s2d_url, json=json_data)
    if response.status_code == 200:
        print("\n==============DESCRIPTION RESPONSE==============\n",
              response.json())
        return response.json()


@app.task(name='tasks.process_story2prompt')
def process_story2prompt(json_data):
    s2p_url = f"{URL}/process_story2prompt"
    response = requests.post(s2p_url, json=json_data)
    if response.status_code == 200:
        print("\n============PROMPTS RESPONSE============\n", response.json())
        return response.json()


@app.task(name='tasks.process_character_generation')
def process_character_generation(json_data):
    character_url = f"{URL}/process_character_generation"
    response = requests.post(character_url, json=json_data)
    if response.status_code == 200:
        print("\n==============CHARACTER RESPONSE==============\n",
              response.json())
        return response.json()


@app.task(name='tasks.process_single_scene')
def process_single_scene(json_data):

    # Make a POST request to the Flask endpoint
    scene_url = f"{URL}/process_single_scene"
    response = requests.post(scene_url, json=json_data)
    # Check if the request was successful
    if response.status_code == 200:
        print("\n=============SCENE RESPONSE=============\n", response.json())
        return response.json()
