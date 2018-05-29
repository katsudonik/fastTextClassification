# fastTextClassification
sample
```
python tweet_get.py __label__1 芸能
python tweet_get.py __label__2 ゲーム
python tweet_get.py __label__3 工事


cat data/__label__1.txt data/__label__2.txt data/__label__3.txt > data/model.txt
python learning.py data/model.txt data/model
python prediction.py キムタク
```
