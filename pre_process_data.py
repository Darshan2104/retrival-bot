import uuid
from src.vector_db import qdrant_client, collection_name
# file_path = 'demo_content.txt'

# with open(file_path, 'r') as file:
#     file_contents = file.read()

def remove_repetitive_lines(input_text):
    lines = input_text.splitlines()
    seen_lines = set()
    result_lines = []
    
    for line in lines:
        if line not in seen_lines:
            result_lines.append(line)
            seen_lines.add(line)
    return "\n".join(result_lines)

def chunk_text(text, source_url, max_chunk_size):
    print("chunk and push to qdrant "+ source_url)
    payload = {
        "uid": str(uuid.uuid4()),
        "content":text,
        "url":source_url
    }
    res = update_qdrant_db(payload)
    chunks = []
    # words = text.split()
    # for i in range(0, len(words), max_chunk_size):
    #     chunk = " ".join(words[i:i + max_chunk_size])
    #     payload = {
    #         "uid": str(uuid.uuid4()),
    #         "content":chunk,
    #         "url":source_url
    #     }
    #     res = update_qdrant_db(payload)
    #     print(source_url," ---> ",res)
    #     chunks.append(payload)
    return chunks


def pre_process_text(file_contents, source_url, max_chunk_size=500):
    file_contents = file_contents.strip()
    print("WE have data with us for "+ str(len(file_contents))+" -->"+ source_url)
    updated_file_contents = remove_repetitive_lines(file_contents)
    # update_qdrant_db = update_qdrant_db(updated_file_contents)
    chunks = chunk_text(updated_file_contents, source_url, max_chunk_size)
    return chunks

def update_qdrant_db(payload):
    rep = qdrant_client.insert_new_data(collection_name, payload)
    return rep
    
