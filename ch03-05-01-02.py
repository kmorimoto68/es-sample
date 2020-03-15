from elasticsearch import Elasticsearch
es = Elasticsearch()

jp_index = 'jp_index'

query = {
    "query": {
        "more_like_this": {
            "fields": ["text"],
            "like": [{
                "_index": "jp_index",
                "_type": "_doc",
                "_id": "3" # _id = app_id = 3: 定山渓温泉
            }]
        }
    }
}

# 検索実行
res = es.search(index = jp_index, body = query)

# 結果表示
w1 = res['hits']['hits']

for item in w1:
    score = item['_score']
    source = item['_source']
    app_id = source['app_id']
    title = source['title']
    print(app_id, title, score)