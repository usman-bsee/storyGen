import datetime
from flask import Flask, request, jsonify
from character_gen import generate_face_image
from scene_gen import generate_scene
from story2prompts import generate_prompts_from_story
from story2prompts import generate_prompt_for_face
from io import BytesIO
from openai import OpenAI
from PIL import Image
import boto3
import json
import os
import re
from model_loading import initialize_ip_adapter
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get("AWS_SECRET_ACCESS_KEY")


celery_file_path = "/home/ubuntu/storyGen/celery-on.txt"
with open(celery_file_path, 'w') as file:
    file.write("0\n")
with open("/home/ubuntu/storyGen/logs_script.txt", 'a') as file:
    file.write(
        f"flaskapp runs at {
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            } and set celery log = 0\n")

local_directory = "stabilityai/stable-diffusion-xl-base-1.0"
ip_model = initialize_ip_adapter(local_directory)


with open(celery_file_path, 'w') as file:
    file.write("1\n")
with open("/home/ubuntu/storyGen/logs_script.txt", 'a') as file:
    file.write(
        f"Model is loaded at {
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")} and set celery log = 1\n\n")


def create_s3_client(region_name):
    return boto3.client('s3', region_name=region_name)


def upload_prompts_to_s3(s3_client, prompts_json, bucket_name, object_name):
    # Upload the file to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=prompts_json,
        ContentType='application/json'
    )


def fetch_image_from_s3(s3_client, bucket_name, object_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    file_content = response['Body'].read()
    image = Image.open(BytesIO(file_content))
    return image


def extract_bucket_and_object(url):
    # Regex to match the S3 URL
    match = re.match(r'https://(.+?)\.s3\.amazonaws\.com/(.+)', url)
    if match:
        bucket_name = match.group(1)
        object_name = match.group(2)
        return bucket_name, object_name
    else:
        return None, None


app = Flask(__name__)


@app.route('/process_story2description', methods=['POST'])
def story2description():    # returns dict
    json_data = request.get_json()
    story = json_data['story']

    face_prompts = generate_prompt_for_face(
        story, client)  # returns is the description of face
    face_prompts_json = json.dumps(face_prompts)
    return {"face_prompts": face_prompts_json}


@app.route('/process_story2prompt', methods=['POST'])
def story2prompt():
    json_data = request.get_json()
    story = json_data['story']
    object_name = json_data['object_name']
    bucket_name = json_data['bucket_name']
    region = json_data.get('region', 'us-east-1')
    s3_client = create_s3_client(region)

    if json_data['no_of_prompts']:
        no_of_prompts = json_data['no_of_prompts']
    else:
        no_of_prompts = 1

    prompts = generate_prompts_from_story(story, client, no_of_prompts)
    prompts_json = json.dumps(prompts)
    upload_prompts_to_s3(s3_client, prompts_json, bucket_name, object_name)
    return {"prompts": prompts_json}


@app.route('/process_character_generation', methods=['POST'])
def character_generation():
    json_data = request.get_json()
    face_prompt = json_data['face_prompt']
    face_object = json_data['face_object']
    bucket_name = json_data['bucket_name']
    region = json_data.get('region', 'us-east-1')
    s3_client = create_s3_client(region)

    buffered = BytesIO()
    image = generate_face_image(face_prompt, client)
    image.save(buffered, format="PNG")
    buffered.seek(0)
    upload_prompts_to_s3(s3_client, buffered.getvalue(),
                         bucket_name, face_object)
    character_url = f"https://{bucket_name}.s3.amazonaws.com/{face_object}"

    return jsonify(character_url)


@app.route('/process_single_scene', methods=['POST'])
def single_scene_generation():
    json_data = request.get_json()
    face_url = json_data['face_url']
    region = json_data.get('region', 'us-east-1')
    single_prompt = json_data['single_prompt']
    age_prompt = json_data['age_gender']
    scene_object = json_data['object_name']
    age_change = json_data['age_change']

    bucket_name, object_name = extract_bucket_and_object(face_url)
    s3_client = create_s3_client(region)
    face = fetch_image_from_s3(s3_client, bucket_name, object_name)
    character_emphasis = "High"

    output_objects = []
    buffered = BytesIO()
    no_of_scenes = []

    # Make a POST request to the Flask endpoint
    images, age_image = generate_scene([single_prompt],
                                       [age_prompt], [face], age_change,
                                       character_emphasis, ip_model)
    output_objects.append(scene_object)
    for image in images:
        image.save(buffered, format="PNG")
        buffered.seek(0)
        upload_prompts_to_s3(
            s3_client,
            buffered.getvalue(),
            bucket_name,
            scene_object)
        no_of_scenes.append(images)
        scene_url = f"https://{bucket_name}.s3.amazonaws.com/{scene_object}"
    return jsonify(scene_url)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5100)
