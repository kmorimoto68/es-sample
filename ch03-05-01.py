title_list = ['菅野温泉','養老牛温泉','定山渓温泉','登別温泉','洞爺湖温泉','ニセコ温泉郷','朝日温泉 (北海道)',
          '酸ヶ湯温泉','蔦温泉', '花巻南温泉峡','夏油温泉','須川高原温泉','鳴子温泉郷','遠刈田温泉','峩々温泉',
           '乳頭温泉郷','後生掛温泉','玉川温泉 (秋田県)','秋ノ宮温泉郷','銀山温泉','瀬見温泉','赤倉温泉 (山形県)',
           '東山温泉','飯坂温泉','二岐温泉','那須温泉郷','塩原温泉郷','鬼怒川温泉','奥鬼怒温泉郷',
           '草津温泉','伊香保温泉','四万温泉','法師温泉','箱根温泉','湯河原温泉',
           '越後湯沢温泉','松之山温泉','大牧温泉','山中温泉','山代温泉','粟津温泉',
           '奈良田温泉','西山温泉 (山梨県)','野沢温泉','湯田中温泉','別所温泉','中房温泉','白骨温泉','小谷温泉',
           '下呂温泉','福地温泉','熱海温泉','伊東温泉','修善寺温泉','湯谷温泉 (愛知県)','榊原温泉','木津温泉',
           '有馬温泉','城崎温泉','湯村温泉 (兵庫県)','十津川温泉','南紀白浜温泉','南紀勝浦温泉','湯の峰温泉','龍神温泉',
           '奥津温泉','湯原温泉','三朝温泉','岩井温泉','関金温泉','玉造温泉','有福温泉','温泉津温泉',
           '湯田温泉','長門湯本温泉','祖谷温泉','道後温泉','二日市温泉 (筑紫野市)','嬉野温泉','武雄温泉',
           '雲仙温泉','小浜温泉','黒川温泉','地獄温泉','垂玉温泉','杖立温泉','日奈久温泉',
           '鉄輪温泉','明礬温泉','由布院温泉','川底温泉','長湯温泉','京町温泉',
           '指宿温泉','霧島温泉郷','新川渓谷温泉郷','栗野岳温泉']

# wikipediaの記事の読み取り
# 2.1節参照
import wikipedia
wikipedia.set_lang("ja")

data_list = []
for index, title in enumerate(title_list):
    print(index+1, title)
    text = wikipedia.page(title,auto_suggest=False).content
    item = {
        'app_id': index+1,
        'title': title,
        'text': text
    }
    data_list.append(item)


# Elasticsearchインスタンスの生成
# 3.3節参照

from elasticsearch import Elasticsearch
es = Elasticsearch()

create_index = {
    "settings": {
        "analysis": {
            "filter": {
                "synonyms_filter": { # 同義語フィルターの定義
                    "type": "synonym",
                    "synonyms": [ #同義語リストの定義 (今は空の状態)
                        ]
                }
            },
            "tokenizer": {
                "kuromoji_w_dic": { # カスタム形態素解析の定義
                "type": "kuromoji_tokenizer", # kromoji_tokenizerをベースにする
                    # ユーザー辞書としてmy_jisho.dicを追加  
                    "user_dictionary": "org/my_jisho.dic" 
                }
            },
            "analyzer": {
                "jpn-search": { # 検索用アナライザーの定義
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer", # 文字単位の正規化
                        "kuromoji_iteration_mark" # 繰り返し文字の正規化
                    ],
                    "tokenizer": "kuromoji_w_dic", # 辞書付きkoromoji形態素解析
                    "filter": [
                        "synonyms_filter", # 同義語展開
                        "kuromoji_baseform", # 活用語の原型化
                        "kuromoji_part_of_speech", # 不要品詞の除去
                        "ja_stop", #不要単語の除去
                        "kuromoji_number", # 数字の正規化
                        "kuromoji_stemmer" #長音の正規化
                    ]
                },
                "jpn-index": { # インデックス生成用アナライザーの定義
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer", # 文字単位の正規化
                        "kuromoji_iteration_mark" # 繰り返し文字の正規化
                    ],
                    "tokenizer": "kuromoji_w_dic", # 辞書付きkoromoji形態素解析
                    "filter": [
                        "kuromoji_baseform", # 活用語の原型化
                        "kuromoji_part_of_speech", # 不要品詞の除去
                        "ja_stop", #不要単語の除去
                        "kuromoji_number", # 数字の正規化
                        "kuromoji_stemmer" #長音の正規化
                    ]
                }
            }
        }
    }
}

# 日本語用インデックス名の定義
jp_index = 'jp_index'

# 同じ名前のインデックスがすでにあれば削除する
if es.indices.exists(index = jp_index):
    es.indices.delete(index = jp_index)

# インデックス jp_doc の生成
es.indices.create(index = jp_index, body = create_index)

mapping =  {
    "properties": {
        "text": {
            "type": "text",
            "analyzer": "jpn-search"
        },
        "title": {
            "type": "text",
            "analyzer": "jpn-search"
        }

    }
}
es.indices.put_mapping(index = jp_index, body = mapping)

for body in data_list:
    # id と app_id の値を同じにして、類似検索をやりやすくする
    es.index(index = jp_index, id = body['app_id'], body = body)
