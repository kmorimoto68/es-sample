# リスト 3.4.1 wikipediaの日本百名湯記事をTF-IDFで分析

# 日本百名湯のうち、Wikipediaに記事のある温泉のリスト

spa_list = ['菅野温泉','養老牛温泉','定山渓温泉','登別温泉','洞爺湖温泉','ニセコ温泉郷','朝日温泉 (北海道)',
          '酸ヶ湯温泉','蔦温泉', '花巻南温泉峡','夏油温泉','須川高原温泉','鳴子温泉郷','遠刈田温泉','峩々温泉',
           #'乳頭温泉郷','後生掛温泉','玉川温泉 (秋田県)','秋ノ宮温泉郷','銀山温泉','瀬見温泉','赤倉温泉 (山形県)',
           #'東山温泉','飯坂温泉','二岐温泉','那須温泉郷','塩原温泉郷','鬼怒川温泉','奥鬼怒温泉郷',
           #'草津温泉','伊香保温泉','四万温泉','法師温泉','箱根温泉','湯河原温泉',
           #'越後湯沢温泉','松之山温泉','大牧温泉','山中温泉','山代温泉','粟津温泉',
           #'奈良田温泉','西山温泉 (山梨県)','野沢温泉','湯田中温泉','別所温泉','中房温泉','白骨温泉','小谷温泉',
           #'下呂温泉','福地温泉','熱海温泉','伊東温泉','修善寺温泉','湯谷温泉 (愛知県)','榊原温泉','木津温泉',
           #'有馬温泉','城崎温泉','湯村温泉 (兵庫県)','十津川温泉','南紀白浜温泉','南紀勝浦温泉','湯の峰温泉','龍神温泉',
           #'奥津温泉','湯原温泉','三朝温泉','岩井温泉','関金温泉','玉造温泉','有福温泉','温泉津温泉',
           #'湯田温泉','長門湯本温泉','祖谷温泉','道後温泉','二日市温泉 (筑紫野市)','嬉野温泉','武雄温泉',
           #'雲仙温泉','小浜温泉','黒川温泉','地獄温泉','垂玉温泉','杖立温泉','日奈久温泉',
           #'鉄輪温泉','明礬温泉','由布院温泉','川底温泉','長湯温泉','京町温泉',
           #'指宿温泉','霧島温泉郷','新川渓谷温泉郷','栗野岳温泉']
]

import wikipedia
wikipedia.set_lang("ja")

content_list = []
for spa in spa_list:
    print(spa)
    content = wikipedia.page(spa,auto_suggest=False).content
    content_list.append(content)

from janome.tokenizer import Tokenizer

# Tokenneizerインスタンスの生成
t = Tokenizer()

# 形態素解析関数の定義
def tokenize(text):
    return [token.base_form for token in t.tokenize(text) 
    if token.part_of_speech.split(',')[0] in['名詞','形容詞']]

words_list = []
for content in content_list:
    words = ' '.join(tokenize(content))
    words = words.replace('==', '')
    words_list.append(words)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(min_df=1, max_df=50)

features = vectorizer.fit_transform(words_list)

terms = vectorizer.get_feature_names()

tfidfs = features.toarray()

def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    sorted_idx = tfidf_array.argsort()
    sorted_idx_rev = sorted_idx[::-1]
    top_n_idx = sorted_idx_rev[:n]
    words = [terms[idx] for idx in top_n_idx]

    return words

for i in range(10):
    print('【' + spa_list[i] + '】')
    for x in extract_feature_words(terms, tfidfs, i, 10):
        print(x, end=' ')
    print()