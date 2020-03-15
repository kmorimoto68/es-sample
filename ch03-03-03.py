from elasticsearch import Elasticsearch
es = Elasticsearch()

# リスト3.3.3 日本語用インデックスの登録
# インデックス作成用JSONの定義

create_index = {
    "settings": {
        "analysis": {
            "filter": {
                "synonyms_filter": {
                    "type": "synonym",
                    "synonyms": [],
                }
            },
            "tokenizer": {
                "kuromoji_w_dic": {
                    "type": "kuromoji_tokenizer",
                    "user_dictionary": "org/my_jisho.dic"
                }
            },
            "analyzer": {
                "jpn-search": {
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer",
                        "kuromoji_iteration_mark"
                    ],
                    "tokenizer": "kuromoji_w_dic",
                    "filter": [
                        "synonyms_filter",
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "ja_stop",
                        "kuromoji_number",
                        "kuromoji_stemmer"
                    ]
                },
                "jpn_index": {
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer",
                        "kuromoji_iteration_mark"
                    ],
                    "tokenizer": "kuromoji_w_dic",
                    "filter": [
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "ja_stop",
                        "kuromoji_number",
                        "kuromoji_stemmer"
                    ]
                }
            }
        }
    }
}

jp_index = 'jp_index'

if es.indices.exists(index = jp_index):
    es.indices.delete(index = jp_index)

es.indices.create(index = jp_index, body = create_index)

def analyse_jp_text(text):
    body = {"analyzer": "jpn-search", "text": text}
    ret = es.indices.analyze(index = jp_index, body=body)
    tokens = ret['tokens']
    tokens2 = [token['token'] for token in tokens]
    return tokens2

print(analyse_jp_text('関数のテスト'))
print(analyse_jp_text('ｱﾊﾟｰﾄ'))
print(analyse_jp_text('㌀'))

print(analyse_jp_text('時々'))
print(analyse_jp_text('こゝろ'))
print(analyse_jp_text('学問のすゝめ'))

print(analyse_jp_text('昨日、飲みに行った。'))

print(analyse_jp_text('この店は寿司がおいしい。'))

print(analyse_jp_text('しかし、これでいいのか迷ってしまう。'))

print(analyse_jp_text('一億二十三'))

print(analyse_jp_text('コンピューターを操作する'))
