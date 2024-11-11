"""
Analystics module:

# Common accross all the clients....
- Customer Sentiment : Can do it with prompt only
- urgency & timeline : Can do with COT prompt only
- churn analysis : Can do it with COT prompt only
- +ve and -ve feedback points from customer : Can do it with COT prompt only


# Specific to customer :
- Direct Suggestions: Feature Request, Issues, Ops request
-->

- mention of competitors  (which, why, context)
--> Based on company get some list of compitors and then check mention of compitition in conversation.

- Customer interaction with components (Product lines/ Modules)
--> Need to think

-  Topics (multi dimensional). Eg. Dovetail, Kraftful.
--> Tagging to conversation.
    - Tagging may vary: so keep a list of tags and based on that check how we can merge it into one tag(for same context).

Hint: Context of zluri, get automatically from its website, help docs, G2 reviews, etc. Refers to things like sitegpt (for agent ref).
"""

from util import get_me_convo_prompt
from vector_db import qdrant_client
# This class will get all the things, we can get from transcript
class Conversation:
    def __init__(self, content, source_company="Zluri"):
        self.json_content = self.get_me_proper_json(content)
        convo_prompt, unique_speaker = get_me_convo_prompt(self.json_content)
        self.conversation_prompt = convo_prompt
        self.total_unique_speakers = unique_speaker
        self.source_company = source_company
    @staticmethod
    def get_me_proper_json(self,text_conversation):
        import re
        import json

        # Regular expression to match each line with speaker, timestamp, and utterance
        pattern = r">>([^\t]+)\t([\d:]+)\n(.+?)(?=\n>>|\Z)"

        conversation = []
        for match in re.finditer(pattern, text_conversation, re.DOTALL):
            speaker, timestamp, utterance = match.groups()
            conversation.append({
                "speaker": speaker.strip(),
                "start_time": timestamp.strip(),
                "utterance": " ".join(utterance.strip().splitlines())
            })

        json_output = json.dumps(conversation, indent=4)
        json_output = json.loads(json_output)
        return json_output
    
    @staticmethod
    def get_me_convo_prompt(json_convo):
        conversation = ""
        total_unique_speakers = []
        for convo in json_convo:
            conversation += f"{convo['speaker']}: {convo['utterance']}\n"
            total_unique_speakers.append(convo['speaker'])
        
        total_unique_speakers = list(set(total_unique_speakers))
        return conversation, total_unique_speakers


# ....Actual Class to get results....
class Analytics:
    def __init__(self,content, sources_company):
        self.convo_obj = Conversation(content, sources_company)
        
        self.client_company_name = None
        self.client_company_representative = []
        
        self.summary_of_call = None
        
        # Generic parameters : 
        self.sentiments = self.get_me_induvidual_sentiments()
        self.positive_keywords = []
        self.negative_keywords = []

        
    def get_me_representatives(self):
        prompt = """

"""     
        prompt = prompt.replace("<conversation>",self.convo_obj.conversation_prompt, "<source_company>",self.convo_obj.source_company)
        return 

    def get_me_induvidual_sentiments(self):
        pass

"""
To-Do : 

- Add module for common analysis.(direct LLM calls).

- For Conversation tagging :
    - Create set of keywords intents from training data (conversation) [ Ask LLM to generate after looking at conversation]
    - After that do the clustering of that.
    - visualize the data how good clusters are
    - Once clusters are finalized, Give each of them one tag.

- churn analysis
    - first we will see the sentiment of customers if negative then only we will process ahead
    - After that we will check for negative keywords and sentences spoken by clients.
    - We will do few short prompting with COT reasoning to do churn analysis, and if customer is leaving what is a major reason.

- Mention of competitors  (which, why, context)
    - For these we need to use Tool like google search.
    - The way we are creating context of companies, we will also add compitition in vectorsDB.
    - If conversation contains something realted to compitition or those companies.
        - We will ask LLM with query why client mention name of company XYZ(compitor) with prompting.

Bonous:        
- Summary of conversation.
"""

if __name__ == "__main__":
    qdrant_client.get_classification_result