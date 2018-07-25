import os

import numpy as np
import jieba
import jieba.analyse
from keras.models import load_model
import pandas as pd
import json

maxlen = 100  # 截断词数
min_count = 5  # 出现次数少于该值的词扔掉。这是最简单的降维方法
module_dir = os.path.dirname(__file__)  # 获取当前目录
model_path = os.path.join(module_dir, 'my_model.h5')

model = load_model(model_path)

jieba.enable_parallel(4)
record_path = os.path.join(module_dir, 'record.json')
with open(record_path, 'r') as load_f:
    content = json.load(load_f)

abc = pd.Series(content).value_counts()
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0  # 添加空字符串用来补全
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    return list(abc[s])


def predict_one(s):  # 单个句子的预测函数
    print(s)
    s = np.array(doc2num(list(jieba.cut(s)), maxlen))
    s = s.reshape((1, s.shape[0]))

    return model.predict_classes(s, verbose=0)[0][0]


def predict_multi(s):
    pos_num = 0
    neg_num = 0
    for i in s:
        tmp = predict_one(i)
        if tmp == 0:
            neg_num = neg_num + 1
        else:
            pos_num = pos_num + 1
    return pos_num * 1.0 / (pos_num + neg_num)


def key_word(s):
    sentences = ""
    for i in s:
        sentences += i
    ans = jieba.analyse.textrank(sentences, topK=30, withWeight=True, allowPOS=['n', 'a'])
    return ans

a = "质量非常差"
b = "电饭锅不能用"
c = "东西很好"
d = [a, b, c]
print(predict_one(a))
print(predict_one(b))
print(predict_one(c))
print(predict_multi(d))
print(key_word(d))
