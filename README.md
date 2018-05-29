# fastTextClassification
sample
```
python tweet_get.py __label__1 芸能
python tweet_get.py __label__2 ゲーム
python tweet_get.py __label__3 工事
cat __label__1.txt __label__2.txt __label__3.txt > model.txt
python learning.py model.txt model
python prediction.py キムタク
```
