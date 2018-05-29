import re
import json
import MeCab
import sys
from requests_oauthlib import OAuth1Session


CK = "gbQOUYjpfcaRbCMKURYvHQCGU"
CS = "7m60spfghq1CuDbNYPBx2GSSw6jUNkGDO73Qr2VPsBt7ClYNOl"
AT = "796922511141146624-zVaxuWmQBJs1cu6gJ2VHGmQ5V5YQfCQ"
AS = "3p4g5QttrbcsRkcv2u6DcTJHfLwVV93Q64f7M7uVL8hVU"

API_URL = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

args = sys.argv
label = args[1]
keyword = args[2]

def main():


    tweets = get_tweet()
    surfaces = get_surfaces(tweets)     #ツイートを分かち書き
    write_txt(surfaces)                 #ツイートを書き込み

def get_tweet():
    """
    TwitterからKEYWORDに関連するツイートを取得
    """
    params = {'q' : keyword, 'count' : 100}
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(API_URL, params = params)
    results = []
    if req.status_code == 200:
        # JSONをパース
        tweets = json.loads(req.text)
        for tweet in tweets['statuses']:
            results.append(tweet['full_text'])
        return results
    else:
        # エラー
        print ("Error: %d" % req.status_code)

def get_surfaces(contents):
    """
    文書を分かち書きし単語単位に分割
    """
    results = []
    for row in contents:
        content = format_text(row)
        tagger = MeCab.Tagger('')
        tagger.parse('')
        surf = []
        node = tagger.parseToNode(content)
        while node:
            surf.append(node.surface)
            node = node.next
        results.append(surf)
    return results

def write_txt(contents):
    """
    評価モデル用のテキストファイルを作成する
    """
    try:
        if(len(contents) > 0):
            fileNeme = "./data/" + label + ".txt"
            labelText = label + ", "

            f = open(fileNeme, 'a')
            for row in contents:
                # 空行区切りの文字列に変換
                spaceTokens = " ".join(row);
                result = labelText + spaceTokens + "\n"
                # 書き込み
                f.write(result)
            f.close()

        print(str(len(contents))+"行を書き込み")

    except Exception as e:
        print("テキストへの書き込みに失敗")
        print(e)

def format_text(text):
    '''
    ツイートから不要な情報を削除
    '''
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub(r'&[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub(';', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('\n', " ", text)
    return text

if __name__ == '__main__':
    main()
