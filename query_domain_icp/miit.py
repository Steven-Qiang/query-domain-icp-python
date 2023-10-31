'''
 @Author StevenQ
 @Github https://github.com/qiangmouren/query-domain-icp-python
 本项目仅供学习交流请勿用于非法用途
'''

import base64
import time
import ddddocr
import requests

"""
    @description: Miit
    @param {int} max_retry 最大重试次数
    @param {bool} debug 是否开启调试模式
    @param {int} retry_sleep 重试间隔
    @example:
        miit = Miit(debug=True, retry_sleep=0)
        list = miit.query("baidu.com")
        print("查询结果：", list)
"""


class Miit:
    def __init__(self, max_retry=5, debug=False, retry_sleep=1):
        self.__baseURL = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/"
        self.__ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        self.__expire = 0
        self.__debug = debug
        self.__max_retry = max_retry
        self.__retry_sleep = retry_sleep
        self.__session = requests.Session()
        self.__session.headers = {
            "Origin": self.__baseURL,
            "Referer": self.__baseURL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

    """
        @description: query 普通查询
        @param {str} unitName 搜索内容
        @param {int} serviceType 服务类型
        @param {int} pageSize 每页数量
        @param {int} pageNum 页码
        @return {*}
    """

    def query(self, unitName, serviceType=1, pageSize=10, pageNum=1, sign=None):
        if unitName == None or unitName == "":
            raise Exception("unitName can not be empty")
        if self.__debug:
            print(
                "query", "unitName", unitName, "pageNum", pageNum, "pageSize", pageSize
            )
        if not self.__session.headers.get("token") or time.time() > self.__expire:
            self.__getToken()
        if sign == None:
            sign = self.__getSign()
        if sign == None:
            raise Exception("Failed to get sign")
        if self.__debug:
            print("query", "sign", sign)
        json = {
            "pageNum": pageNum,
            "pageSize": pageSize,
            "serviceType": serviceType,
            "unitName": unitName,
        }
        resp = self.__session.post(
            self.__baseURL + "icpAbbreviateInfo/queryByCondition",
            json=json,
            headers={"sign": sign, "Content-Type": "application/json"},
        ).json()
        if resp["success"] == False:
            raise Exception("Failed to query")
        return {
            "sign": sign,
            "list": resp["params"]["list"],
            "total": resp["params"]["total"],
            "pages": resp["params"]["pages"],
            "nextPage": resp["params"]["nextPage"],
        }

    """
        @description: getNextPage 获取下一页
        @param {str} unitName 搜索内容
        @param {str} sign 签名 （从第一次的query中获取）
        @param {int} serviceType 服务类型
        @param {int} pageSize 每页数量
        @param {int} pageNum 页码
        @return {*}
    """

    def getNextPage(self, unitName, sign, serviceType=1, pageSize=10, pageNum=1):
        return self.query(unitName, serviceType, pageSize, pageNum, sign)

    def __getToken(self):
        auth = self.__session.post(
            self.__baseURL + "auth",
            {
                "authKey": "3c81474a37688b1971355eaed4898229",
                "timeStamp": "1698737110659",
            },
        ).json()
        expire = auth["params"]["expire"]
        token = auth["params"]["bussiness"]
        self.__session.headers.update({"token": token})
        self.__expire = time.time() + expire
        if self.__debug:
            print("__getToken", "token:", token, "expire:", expire)

    def __getSign(self):
        _retry = 0
        while _retry < self.__max_retry:
            if self.__debug:
                print("__getSign", "_retry", _retry)
            resp = self.__session.post(self.__baseURL + "image/getCheckImage").json()
            if self.__debug:
                print("__getSign", "getCheckImage", resp["params"]["uuid"])
            if resp["success"] == False:
                _retry += 1
                time.sleep(self.__retry_sleep)
                continue
            bigImage = base64.b64decode(resp["params"]["bigImage"])
            smallImage = base64.b64decode(resp["params"]["smallImage"])
            match = self.__ocr.slide_match(smallImage, bigImage, simple_target=True)
            resp = self.__session.post(
                self.__baseURL + "image/checkImage",
                json={
                    "key": resp["params"]["uuid"],
                    "value": int(match["target"][0]) + 2,
                },
                headers={"Content-Type": "application/json"},
            ).json()
            if self.__debug:
                print("__getSign", "checkImage", resp)
            if resp["success"] == False:
                _retry += 1
                time.sleep(self.__retry_sleep)
                continue
            return resp["params"]
        raise Exception("Failed to get sign")
