#encoding=utf-8
import os
#项目的绝对路径
projectDir=os.path.dirname(os.path.dirname(__file__))

#数据文件的绝对路径
file_path=projectDir + "\\testData\\inter_test_data.xlsx"

#API sheet中所需列号
API_apiName=2
API_requestUrl=3
API_requestMethod=4
API_paramsType=5
API_apiCaseSheetName=6
API_ifExecute=7

#接口用例sheet中所需列号
CASE_requestData=1
CASE_relyRule=2
CASE_responseData=3
CASE_checkPoint=4
CASE_ifExecute=5
CASE_result=6
CASE_errorInfo=7

#存储请求参数里的依赖数据
REQUEST_DATA = {}

#存储响应对象中的依赖数据
RESPONSE_DATA = {}


if __name__== '__main__':
    print projectDir
    print file_path