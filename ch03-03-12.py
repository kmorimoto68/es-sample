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
                    "synonyms": [
                        "すし,スシ,鮨,寿司"
                    ],
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
                "jpn-index": {
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

if es.indices.exists(index=jp_index):
    es.indices.delete(index=jp_index)

es.indices.create(index=jp_index, body=create_index)

def analyse_jp_text(text):
    body = {"analyzer": "jpn-search", "text": text}
    ret = es.indices.analyze(index=jp_index, body=body)
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

mapping = {
    "properties": {
        "content": {
            "type": "text",
            "analyzer": "jpn-index",
            "search_analyzer": "jpn-search"
        }
    }
}

print(es.indices.put_mapping(index=jp_index, body=mapping))

# リスト 3.3.13 日本語文書の投入

bodys = [
    { "title": "山田太郎の紹介",
    "name": {
        "last": "山田",
        "first": "太郎"
    },
    "content": "スシが好物です。犬も好きです。"},
    { "title": "田中次郎の紹介",
    "name": {
        "last": "田中",
        "first": "次郎"
    },
    "content": "そばがだいすきです。ねこもだいすきです。"},
    { "title": "渡辺三郎の紹介",
    "name": {
        "last": "渡辺",
        "first": "三郎"
    },
    "content": "天ぷらが好きです。新幹線はやぶさのファンです。"}
]

for i, body in enumerate(bodys):
    es.index(index=jp_index, id=i, body=body)
