
def get_me_proper_json(text_conversation):
    import re
    import json

    # Regular expression to match each line with speaker, timestamp, and utterance
    pattern = r">>([^\t]+)\t([\d:]+)\n(.+?)(?=\n>>|\Z)"

    # Parse and store results
    conversation = []
    for match in re.finditer(pattern, text_conversation, re.DOTALL):
        speaker, timestamp, utterance = match.groups()
        conversation.append({
            "speaker": speaker.strip(),
            "start_time": timestamp.strip(),
            "utterance": " ".join(utterance.strip().splitlines())
        })

    # Convert to JSON
    json_output = json.dumps(conversation, indent=4)
    # print(json_output)
    json_output = json.loads(json_output)
    return json_output

def get_me_convo_prompt(json_convo):
    conversation = ""
    total_unique_speakers = []
    for convo in json_convo:
        conversation += f"{convo['speaker']}: {convo['utterance']}\n"
        total_unique_speakers.append(convo['speaker'])
    
    total_unique_speakers = list(set(total_unique_speakers))
    return conversation, total_unique_speakers

# Speakers dilatation.... in case of need
def get_the_person_who_is_from_source_org(conversation, source_org=""):
    # based on words (n-gram)
    # or directly through LLM :)
    pass

if __name__ == "__main__":
    # Input text
    text = """
    >>Roy Baby Thachil	00:00
    My name is Roy, I have been in partnerships in Zuludi, been working with the company for the past three years, I was an Sdr, worked in US and India markets. And currently, we thought that we need presence in the market and that's how we formed the partnership department a year back. And currently I'm running it with my management above me. So that's a bit, a quick intro about me. I would love if you could give me a quick intro and how you came to know about Zuludi and what type of partnership are you looking for?

    >>Justin Mathews	00:32
    So before me, I, you know, so I lead the partnerships team at CookyS. And what CookyS is basically, we are a global leader in the consent management platform category...
    """

    json_convo = get_me_proper_json(text)
    print(get_me_convo_prompt(json_convo))