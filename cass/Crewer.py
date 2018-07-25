import multiprocessing
import time
import requests
import datetime


class Crewer:
    def __init__(self):
        self.NoneComment = '此用户没有填写评论!'
        self.DefaultComment = '评价方未及时作出评价，系统默认好评。'
        self.Error = 'error'

    def getId(self, url):
        # 通过url 获取商品id
        return url.split('&id=')[1].split('&')[0]

    def spider(self, url):
        # 爬虫方法
        try:
            resp = requests.get(url)
        except requests.exceptions.MissingSchema:
            print("链接无法访问！")
            return False
        htmlStr = resp.text
        if self.isUrlValid(htmlStr, url):
            print("链接有效，评论爬虫开始！")
        else:
            print("链接无效！")
            return False
        urlBase1 = 'http://rate.tmall.com/list_detail_rate.htm?itemId='
        urlBase2 = '&sellerId='
        urlBase3 = '&currentPage='
        urlKey1 = self.getId(url)
        urlKey2 = htmlStr.split('sellerId=')[1].split('&')[0]
        jsonUrl = urlBase1 + urlKey1 + urlBase2 + urlKey2 + urlBase3
        print(jsonUrl)
        page1 = ""
        try:
            print("开始请求")
            page1 = requests.get(jsonUrl + '1').text
        except ConnectionError:
            print("获取页数出现错误！")
        while len(page1.split('"lastPage":', 1)) is not 2:
            page1 = requests.get(jsonUrl + '1').text
            time.sleep(2)
        allPage = page1.split('"lastPage":', 1)[1].split(',', 1)[0]
        allPage = int(allPage)
        print("总页数为" + str(allPage))
        res = []

        # 创建进程吃进行多进程爬虫
        print("创建进程池")
        pool = multiprocessing.Pool(processes=10)
        print("创建进程池成功！")
        for i in range(1, allPage + 1):
            print("添加进程")
            re = pool.apply_async(self.crewJson, (jsonUrl, i, urlKey1))
            res.append(re)

        pool.close()
        pool.join()
        comments = []
        for j in res:
            for k in j.get():
                comments.append(k)
        print("主进程运行完毕！爬虫完毕！")
        print(comments)
        return comments

    def crewJson(self, jsonUrl, pageNum, id):
        print("正在爬去第" + str(pageNum) + "页")
        finalUrl = jsonUrl + str(pageNum)
        json = requests.get(finalUrl)
        print("爬完第" + str(pageNum) + "页")
        rec = self.jsonToText(json, pageNum)
        ans = rec[0]
        return ans

    def jsonToText(self, json, pageNum):
        # 提取json对应的字符串
        jsonStr = json.text
        re = []
        i = 1
        while i > 0:
            try:
                jsonStr = jsonStr.split('"rateContent":"', 1)[1]
            except Exception as e:
                i = i - 1
                break
            # 进行简单的数据清洗
            ans = jsonStr.split('"')[0]
            ans = ans.replace('<b></b>', '')
            ans = ans.replace('&hellip;', '')

            if ans == self.NoneComment or ans == self.DefaultComment:
                continue
            else:
                i = i + 1
                re.append(ans)

        if i == 0:
            print("此页面无评论信息")
        else:
            print(str(pageNum) + "页有" + str(i) + "条评论信息！")
        return [re, i]

    def isUrlValid(self, htmlstr, url):
        # 验证当前获取的链接是否有效
        if (url.find('&id=') is not -1) and (htmlstr.find('sellerId')):
            return True
        else:
            return False


if __name__ == '__main__':
    beginTime = datetime.datetime.now()
    cre = Crewer()
    url = input('请输入需要分析的商品链接:\n')
    result = cre.spider(url)
    while result is False:
        url = input('请输入需要分析的商品链接:\n')
        result = cre.spider(url)

    Time = datetime.datetime.now() - beginTime
    print(str(Time))
