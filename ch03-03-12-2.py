from elasticsearch import Elasticsearch
es = Elasticsearch()

jp_index = 'jp_index'


# リスト 3.3.14 日本語文書の検索
query = {
    "query": {
        "match": {
            "content": "ｽｼ"
        }
    }
}

res = es.search(index=jp_index, body=query)

import json
print(json.dumps(res, indent=2, ensure_ascii=False))

# リスト 3.3.14 日本語文書の検索
query = {
    "query": {
        "match": {
            "content": "はやぶさ"
        }
    }
}

res = es.search(index=jp_index, body=query)

print(json.dumps(res, indent=2, ensure_ascii=False))
