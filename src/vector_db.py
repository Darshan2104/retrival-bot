import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, Filter
from sentence_transformers import SentenceTransformer
from loguru import logger as log
from src.constants import QDRANT_URL, API_KEY

# collection_name = "zluri_entire_data"
collection_name = "zluri_final"
class qdrantDB:
    def __init__(self) :

        self.dimension = 384 #768

        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.get_embedding = lambda x: self.model.encode(x).tolist()
            #Establishing connection to qdrant db
            self._conn = self.connect_to_db()

            if self._conn == None:
                log.error(f'Error connecting to qdrant DB')

        except BaseException as e:
            log.error("Exception When trying to connect to qdrant Database : " + str(e))

    def connect_to_db(self):
        try:
            # _conn = QdrantClient(url=self.url, port=self.port, api_key=self.api_key)
            _conn = QdrantClient(url=QDRANT_URL, api_key=API_KEY)
            return _conn

        except Exception as e:
            log.exception(f"Exception when connecting to DB: {e}")
            return None

    def get_classification_result(self, collection_name ,query, top_k=3):
        status = "success"
        try:
            query_embedding = self.get_embedding(query)
            
            search_result = self._conn.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=top_k
            )
            results = [
                {
                    "url": hit.payload.get('url'),
                    "content": hit.payload.get('content'),
                    "header": hit.payload.get('header'),
                    "score": hit.score,
                    "ticket_id": hit.payload.get('ticket_id')
                }
                for hit in search_result
            ]
            sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
            
            return {"status":status,
             "results":{
                "matches": sorted_results
            }
             }
            
        except Exception as e:
            status = "failure"
            log.exception(f"Error get_classification_result ---> {str(e)}")
            return {"status":status,"message":str(e)}

        
    def insert_new_data(self, collection_name, payload):
        status = "success"
        try:
            uid = payload.get("uid")
            ticket_id = str(payload.get("uid"))
            content = payload.get("content")
            url = payload.get("url")
            header = payload.get("header")
            embedding = self.get_embedding(content)
            
            updated_payload = {
                "uid":uid,
                "ticket_id":ticket_id,
                "header":header,
                "content":content,
                "url":url
            }

            point = PointStruct(id=ticket_id, vector=embedding, payload=updated_payload)
            self._conn.upsert(
                collection_name=collection_name,
                points=[point]
            )
            log.info(f"ticker id {ticket_id} added successfully")
            return {"status": status,"message":"New data added successfully"}
        except Exception as e:
            status = "failure"
            log.exception(f"Exception in qdrant upsert --> {str(e)}")
            return {"status":status}

    def get_specific_data(self, collection_name, ticket_id):
        status = "success"
        try:
            response = self._conn.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                        must=[
                            {
                                "key": "ticket_id",
                                "match": {
                                    "value": ticket_id
                                }
                            }
                        ]
                    )
                )
            
            if response[0]: 
                payload = response[0][0]
                return {
                    "status":status,
                    "result":payload
                }
                
            else:
                return {"status":status,"message":"Ticket id not found"}
        except Exception as e:
            status = "failure"
            log.exception(f"Exception in qdrant get_specific_data --> {str(e)}")
            return {"status":status}

    
    def delete_specific_data(self, collection_name, ticket_id):
        status = "success"
        try:    
            self._conn.delete(
                collection_name=collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="ticket_id",
                                match=models.MatchValue(value=ticket_id) 
                            ),
                        ],
                    )
                ),
            )
            return {"status":status,"message":"Data deleted sucessfully"}
        except Exception as e:
            status = "failure"
            log.exception(f"Exception in qdrant delete_specific_data --> {str(e)}")
            return {"status":status}

    def update_specific_data(self, collection_name, ticket_id, updated_payload):
        status = "success"
        try:
            resp = self.delete_specific_data(collection_name, ticket_id)
            resp = self.insert_new_data(collection_name,updated_payload)
            return {"status": status,"message":"Data Updated added successfully"}
        except Exception as e:
            status = "failure"
            log.exception(f"Exception in qdrant update_specific_data --> {str(e)}")
            return {"status":status}

    def create_collection(self, collection_name):
        status = "success"
        try:
            res = self._conn.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=self.dimension, distance=models.Distance.COSINE),
            )

            log.info(f"{collection_name} recreated successfully")
            return status
        except Exception as e:
            status = "failure"
            log.exception(f"Exception in qdrant recreate_collection --> {str(e)}")
            return status
        
    def delete_collection(self, collection_name):
        try:
            log.info(f"deleting {collection_name}")
            res = self._conn.delete_collection(collection_name="{collection_name}")
            log.info(f"successfuly deleted {collection_name}")

            return str(res)
        
        except Exception as e:
            log.exception(f"Exception in qdrant delete_collection ---> {str(e)}")
            return ""


    def get_collections(self):
        try:
            log.info("fetching all available collections")
            res = self._conn.get_collections()

            return str(res)
        
        except Exception as e:
            log.exception(f"Exception in get_collection ---> {str(e)}")
            return ""


    def get_collection(self, collection_name):
        try:
            log.info("fetching collection details")
            res = self._conn.get_collection(collection_name=collection_name)

            return res
        
        except Exception as e:
            log.exception(f"Exception in get_collection ---> {str(e)}")
            return ""
        

qdrant_client = qdrantDB()
log.info(qdrant_client)

if __name__ == '__main__':
    
    qdrant_client = qdrantDB()
    collection_name = "zluri_final"
    # qdrant_client.create_collection(collection_name)
    
    # import json
    # file_path = 'result.json'

    # with open(file_path, 'r') as file:
    #     data = json.load(file)

    # for d in data["data"]:
    #     res = qdrant_client.insert_new_data(collection_name, d)
    #     print(res)

    # our_collection = qdrant_client.get_collection(collection_name)
    # log.info(our_collection)
    query =  "how to integrate Jira on zluri"
    res = qdrant_client.get_classification_result(collection_name ,query, top_k=3)
    print(res)