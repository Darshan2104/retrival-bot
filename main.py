"""
- Get the Conversation.
- Based on Companie name get the latest details about that company.(Scrap modul)
- For now we will consider entire conversation to get the results[As conversation is huge, We can chunk it and then check for features (improvement part)].
"""

from glob import glob
from src.util import get_me_proper_json, get_me_convo_prompt
import os
from src.analysis import Analytics
main_folder ="data_to_process/Transcripts/"
source_company_name = "zluri"

for folder_name in os.listdir(main_folder):
    folder_path = os.path.join(main_folder, folder_name)
    
    # Check if it is a directory
    if os.path.isdir(folder_path):
        # List all files in the directory
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Open and read each file
            with open(file_path, 'r') as file:
                content = file.read()

        # process the content
        anna = Analytics(content, source_company_name)
        
    break