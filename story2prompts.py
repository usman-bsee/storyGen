import json


def generate_prompts_from_story(story, client, no_of_prompts=''):

    # Each prompt should mention the whether character is young, middle age,
    # old. Keep the character sames as in story in each prompt.
    system1 = f"""
    This system converts a story into a list of DALLE prompts
    for scene visualization.
    **Instructions:**
    1. Convert a story into exactly a list of {no_of_prompts} DALLE prompts.
    2. Make sure that generated prompts must NOT be more than {no_of_prompts}.
    2. Order prompts chronologically.
    3. Include character names with species (e.g., Penelope the panda).
    4. Use format "Penelope the panda" (not "Penelope, the panda").
    5. Don't mention the same character twice in a prompt.
    6. Always use "Penelope the panda" format for character references.
    7. Make sure to mention the character in the corrected format.
    8. Do NOT make any mistake in mentioning the character.
    9. Limit prompts to 30 tokens (words + special characters).
    10. You must follow the token limit at ANY cost.
    11. Make sure that generated prompt should NOT exceed the 30 tokens limit.
    12. Ensure prompts are meaningful and story-related.
    13. Return JSON data with a single key named "prompts".
    14. Each prompt object should have a "prompt" key.
    """

    system2 = """

    **Example:**
    story = In a land painted with lavender sunsets and meadows
    sprinkled with glitterdust, lived a tiny firefly named Flick.
    Flick wasn't like other fireflies. While his friends twinkled
    a soft yellow, Flick's light sputtered a dull orange. He longed
    to illuminate the night sky with a vibrant glow, but his spark
    remained weak. One day, a wise old owl named Hoots hooted down
    from a blossom-laden branch. Flick confided in him, his voice
    trembling like a flickering flame. Hoots listened patiently,
    his large eyes gleaming with ancient wisdom. "Little Flick," he
    hooted softly, "the brightest light comes from within.
    You must find the Moonstone Lake, hidden deep in Whispering Woods."
    Intrigued, Flick set off that very night. Whispering Woods shimmered
    with bioluminescent mushrooms and fireflies with dazzling displays.
    Flick felt a pang of envy, but Hoots' words echoed in his mind. After
    hours of searching, he stumbled upon a clearing bathed in moonlight.
    In its center, a crystal-clear lake shimmered with a million tiny,
    silver stars. It was Moonstone Lake! Hesitantly, Flick dipped his
    tail into the water. A jolt of energy surged through him, and when
    he lifted his tail, it blazed with a brilliant silver light! He
    dipped again and again, his glow growing stronger, surpassing
    anything he'd ever imagined. Overjoyed, Flick returned to his meadow.
    His friends gasped in awe as he lit up the night with a dazzling celestial
    glow. But Flick noticed something even more beautiful – his light wasn't
    just bright, it cast a gentle, calming aura on everything it touched.
    The flowers bloomed brighter, the dewdrops sparkled like diamonds, and a
    chorus of happy chirps filled the air. From that day on, Flick became
    known as the Moonstone Firefly. He learned that true beauty came not
    from trying to be like others, but from embracing his unique light.
    And with that light, he filled his world with not just brightness,
    but with a touch of magic.
    Output:
    The XYZ will be replaced with the prompts generated for the story.
    The format should NOT be compromised.
    ```json
    {"prompts": [{"prompt": "Flick the firely, **--remaining prompt**"},
                 {"prompt": "Flick the firefly, **--remaining prompt**"},
                 {"prompt": "Flick the firefly, **--remaining prompt**"},
                 {"prompt": "Flick the firefly, **--remaining prompt**"},
                 {"prompt": "Flick the firefly, **--remaining prompt**"}]}
    """

    system = system1 + system2

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": story},
        ],
        response_format={"type": "json_object"}
    )

    output = response.choices[0].message.content
    prompts = json.loads(output)

    return prompts


def generate_prompt_for_face(story, client):

    face_system = """
    You are an expert storyteller describing the facial features of
    characters from a story.

    **Instructions:**
    1. You should identify the main character of story and generate prompts.
    2. The generated prompt should be for the main character of the story.
    3. The character can be anything:
                    human, animal, mythical creature, or even an alien!
    4. For humans, specify their age and gender (if possible from the story).
    5. Capture the essence of the character through their facial features.
    6. Consider the character's species, role in story, and the overall tone.
    7. Focus on details that bring the character's face to life, including:
        * **Shape:** Round, oval, square, heart-shaped, etc. (for humanoids)
        * **Eyes:** Color, shape (round, almond, hooded), size (large, small)
        * **Nose:** Shape (broad, button, hooked, beak-like for birds, etc.)
        * **Mouth:** Shape, expression (smiling, sharp fangs for predators)
        * **Skin/Fur/Scales/Feathers (depending on species):**
                    Color, texture (smooth, wrinkled, furry, feathered)
        * **Hair (if applicable):** Color, texture (straight, curly)
        * **Facial Hair (for humanoids):** Mustache, beard, sideburns
        * **Distinguishing Features (optional):** Scars, freckles,
                    wrinkles, pronounced brow ridges, horns,
                    bioluminescent markings (for aliens)
    8. Exclude details about names, clothing, or body type.
    9. Limit prompts to 20 tokens (words + special characters).
    10. You must follow the token limit at ANY cost.
    11. Make sure that generated prompt should NOT exceed the 20 tokens limit.
    12. You should NOT mention about the scenes or the story or the background.
    13. You just need to mention the character description in the prompt.
    14. You should NOT divide this prompt. It should return only ONE prompt.
    15. Add all the description in one SINGLE prompt.

    **Output:**
    Generate a JSON object with a single key: 'face_prompt'.
    The value should be a string containing the detailed face
    description using the above criteria.

    **Example Output (Human):**
    {'face_prompt': "A weathered old man with a square jaw, kind eyes that crinkle at the corners when he smiles, and a bushy white beard."}

    **Example Output (Animal):**
    {'face_prompt': "A cunning fox with a triangular face, sharp amber eyes, and a pointed muzzle with long whiskers twitching inquisitively."}

    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": face_system},
            {"role": "user", "content": story},
        ],
        response_format={"type": "json_object"}
    )
    print("RESPONSE:", response)
    output = response.choices[0].message.content
    face_description = json.loads(output)
    face_key = list(face_description.keys())[0]
    return face_description[face_key]
