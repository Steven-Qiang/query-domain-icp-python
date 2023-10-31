"""
 @Author StevenQ
 @Github https://github.com/qiangmouren/query-domain-icp-python
 本项目仅供学习交流请勿用于非法用途
"""
import json
from query_domain_icp import Miit

miit = Miit(debug=False, retry_sleep=0)
while True:
    unitName = input("请输入单位名称：")
    result = miit.query(unitName)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    pageNum = 1
    while True:
        if result["pages"] > result["nextPage"]:
            input("按回车继续查询下一页,共%d页,当前第%d页" % (result["pages"], pageNum))
            result = miit.getNextPage(unitName, sign=result["sign"], pageNum=pageNum)
            pageNum = result["nextPage"]
            print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            break
