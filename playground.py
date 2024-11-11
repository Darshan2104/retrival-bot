from get_content_from_site import get_me_content
from pre_process_data import pre_process_text
# get_me_content(single_url)

file_path = 'sublinks.txt'

with open(file_path, 'r') as file:
    file_contents = file.read()


source_links = file_contents.split('\n')

overall_chunks = []
flag = False
for single_url in source_links:
    # if flag:
    print(f'Processing: {single_url}')
    content = get_me_content(single_url)
    chunks_payload = pre_process_text(content, single_url, max_chunk_size=500)
    overall_chunks.extend(chunks_payload)
    # else:
    #     print(f'{single_url} already processed')

    

# print(len(overall_chunks))
# print(overall_chunks)