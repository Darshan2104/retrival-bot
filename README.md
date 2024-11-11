# retrival-bot

- app.py : to add your query
- src/llm : It contains context retrival based on user query and llm api to get response
- src/vector_db.py : It contains code related to qdrant
- new_scraper.py : It is used for scraping website.
- get_all_source_links.py : Is is used to get all the possible link/sublink from website

- result.json : Scraped result
- sublinks.txt: Contains all the links/sublinks



- steps to follow:
1. pip install -r requirements.txt
2. Go to app.py and write your query
3. Run python app.py