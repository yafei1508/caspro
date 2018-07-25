from datetime import datetime

from cass.Crewer import Crewer
from cass.DBHelper import DBHelper
from cass.predict import predict_multi, key_word

db = DBHelper()


def analysis(url):
    id = int(url.split('&id=')[1].split('&')[0])
    res = get_score_in_db(url)
    print(len(url.split('&id=')[1].split('&')[0]))
    if res is False:
        crewer = Crewer()
        comments = crewer.spider(url)
        score = predict_multi(comments)
        keywords = key_word(comments)
        insert_score(id, score)
        insert_keywords(id, keywords)
        return [score, keywords]
    else:
        # 如果上一次更新时间大于一天就再次，否则用之前分析的结果
        if (datetime.now() - res[2]).days > 1:
            crewer = Crewer()
            comments = crewer.spider(url)
            score = predict_multi(comments)
            keywords = key_word(comments)
            update_score(id, score)
            update_keywords(id, keywords)
            return [score, keywords]
        else:
            keywords = get_keywords(id)
            return [res[1], keywords]


def get_score_in_db(url):
    id = int(url.split('&id=')[1].split('&')[0])
    sql = "select id, score, update_time from score where id = %s "
    re = db.fetchall(sql, (id,))
    if len(re) is 0:
        return False
    else:
        return re[0]


def update_score(id, score):
    sql = "update score set score = %s where id = %s"
    db.execute(sql, (score, id))


def update_keywords(id, keywords):
    sql = "delete from keywords where sid = %s"
    db.execute(sql, (id,))
    insert_keywords(id, keywords)


def get_keywords(id):
    sql = "select keyword, num from keywords where sid = %s"
    return db.fetchall(sql, (id,))


def insert_score(id, score):
    sql = "insert into score(id, score) values (%s, %s)"
    print(type(id))
    print(type(score))
    db.execute(sql, (id, score))


def insert_keywords(id, keywords):
    for k in keywords:
        sql = "insert into keywords(sid, keyword, num) values (%s,%s,%s)"
        db.execute(sql, (id, k[0], k[1]))

# get_score_in_db('https://detail.tmall.com/item.htm?id=567594121010&ali_refid=a3_430583_1006:1103880035:N:%E8%93%9D%E7%89%99%E8%80%B3%E6%9C%BA:e82a2cb78b05f57a2a8179d50a65ca75&ali_trackid=1_e82a2cb78b05f57a2a8179d50a65ca75&spm=a230r.1.14.1&sku_properties=5919063:6536025')

# update_score(564618187430, 0.333333333344)
