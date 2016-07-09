from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': "localhost", 'port': 9200}])
# create index if it's not in the database
if not es.indices.exists('rr_products'):
    settings = {
        "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
        },
        "mappings": {
            "list":{
                "properties": {
                    "location": { "type": "geo_point"},
                }
            }
        }
    }
    # create index
    es.indices.create(index='rr_products', ignore=400, body=settings)
