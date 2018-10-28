# encoding=utf-8

from util.ParseExcel import *
import os
from config.config import *
import json
from util.md5_encrypt import *

class GetRequestData(object):
    def __init__(self):
        pass

    @classmethod
    def getRequestData(cls, relyRule):
        pe = ParseExcel()
        pe.loadWorkBook(file_path)
        requestData = {}
        # relySource = {"token": "", "userid": "","articleid":""}
        # relyRule = {"token":"userRegister->1->request","userid":"register->1->response","articleid":"userLogin->1->response->['data'][0]"}
        interDict = {"userRegister": "register",
                     "userLogin": "login",
                     "searchUserBlog": "search",
                     "modifyBlog": "modify",
                     "addBlog": "addBlog"}
        dataTypeColDict = {"request": CASE_requestData,
                           "response": CASE_responseData}
        # 根据接口名映射一个字典，对应接口sheet名称
        # 获取到依赖接口的sheet页，case号（行号），请求列或者响应列号，
        # 然后到对应单元格取数据，转成字典格式，
        # 取出里面对应层级的数据
        for key, value in relyRule.items():  # "articleid":"userLogin->1->response->['data'][0]"
            print "key:value==>", key, ":", value
            rList = value.split("->")
            print "len(rList):", len(rList)
            if len(rList) == 4:
                # 说明所需数据在依赖数据的第二层
                interfaceType, caseNo, dataType, dataKey = rList
                # print "interfaceType,caseNo,dataType,dataKey:",interfaceType,',',caseNo,',',dataType,',',dataKey
                # print "interDict[interfaceType]:",interDict[interfaceType]
                # print "dataTypeColDict[dataType]:",dataTypeColDict[dataType]
                interSheetObj = pe.getSheetByName(interDict[interfaceType])
                # print "interSheetObj:",interSheetObj
                relyContent = json.loads(
                    pe.getValueInCell(interSheetObj, rowNo=int(caseNo) + 1, colNo=dataTypeColDict[dataType]))
                # print "relyContent:",relyContent
                # print "type(relyContent):",type(relyContent)
                command = "%s%s['%s']" % (relyContent, dataKey, key)
                # print "command:",command
                requestData[key] = eval(command)
                print "requestData-3:",requestData
            elif len(rList) == 3:
                # 说明所需数据在依赖数据的第一层
                # "token":"userLogin->1->response"
                interfaceType, caseNo, dataType = rList
                # print "interfaceType,caseNo,dataType:",interfaceType,',',caseNo,',',dataType
                # print "interDict[interfaceType]:",interDict[interfaceType]
                # print "dataTypeColDict[dataType]:",dataTypeColDict[dataType]
                interSheetObj = pe.getSheetByName(interDict[interfaceType])
                # print "interSheetObj:",interSheetObj
                contentStr = '%s' % pe.getValueInCell(interSheetObj, rowNo=int(caseNo) + 1,
                                                      colNo=dataTypeColDict[dataType])
                print "contentStr:", contentStr
                print "type(contentStr):", type(contentStr)
                relyContent = json.loads(contentStr)
                print "relyContent:", relyContent
                # print "type(relyContent):",type(relyContent)
                command = "%s['%s']" % (relyContent, key)
                # print "command:",command
                print "key:eval(command):",key,eval(command)
                requestData[key] = md5_encrypt(eval(command)) if key == "password" else eval(command)
                print "requestData-1:",requestData
            else:
                requestData[key] = value
        return requestData


if __name__ == "__main__":
    relyRule = {"articleId": "searchUserBlog->1->response->['data'][0]", "password": "userRegister->1->request",
                "content": "xiaxiaoxu"}
    print GetRequestData.getRequestData(relyRule)

