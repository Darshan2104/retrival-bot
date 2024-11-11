from src.constants import OAI
def get_context(user_query):
    from src.vector_db import qdrant_client
    collection_name = "zluri_final"

    resp = qdrant_client.get_classification_result(collection_name, user_query, top_k=5)

    context = ""
    
    for d in resp["results"]["matches"]:
        content = d["content"].strip()
        # content = content.replace("\n", " ")
        context+= """
Header : <header>
Related Content : <content>

        """.replace("<content>",content).replace("<header>",d["header"])
    
    return context
        

def oai_response(message):
    import json
    import requests

    token = OAI 
    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({"model": "gpt-4o-mini",
                            "messages": message,
                            "temperature": 0,
                            "top_p": 1
                            })
    headers = {'Content-Type': 'application/json','Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    Assistant = response_json['choices'][0]['message']['content']
    token_length = response_json['usage']['total_tokens']
    return Assistant

# prompt = "Tell me a joke in one line"
# system_prompt = ""
# message = [{"role": "system","content": system_prompt},{"role": "user","content": prompt}]

# print(oai_response(message))


def get_me_result(user_query, context):
    system_prompt = """
You are smart Asssitant. Customer is using zluri platform and has asked query related to it. You are given an query and it's related context.
Your task is to first check if that query is related to zluri or not.
If it is not related to zluri, simplly response, 'I can not help you with this.'
If it is related to zluri, proceed with the following steps.
- Use below context related to query.
- analyse what exactly use is asking related to zluri.
- search for that information in context.
- If you find solution, return it to user.
- Make sure whatevery information you will return is accurate.

Context:
<context>
"""


    prompt = """
Respond to the question below with the following format:
Reasoning (e.g. Step N...). for each new reasoning step, Keep a knowledge of previous reasoning steps to do better reasoning.
Question:
From given user query, use your context and answer back to user.
Finally, return me only final response.

User Query:
<query>

Do reasoning 3 times from different perspective and update a final answered based on collective reasoning.After doing reasoning verify the result is relevant to user qeury, based on that update your results and return me final response.

Note: 
- Make sure your result contain only final response with in 200 words.
- Do not include un-necessay things in your response.
- Do not include reasoing steps in your response.
"""


    system_prompt = system_prompt.replace("<context>",context)
    prompt = prompt.replace("<query>",user_query)

    message = [{"role": "system","content": system_prompt},{"role": "user","content": prompt}]
    respnse = oai_response(message)
    return respnse


if __name__ == "__main__":
    user_query = "can i integrate Jira on zluri if so how ?"
    context = get_context(user_query)
    result = get_me_result(user_query, context)
    print(result)