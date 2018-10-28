#encoding=utf-8
import requests
import json
from util.ParseExcel import *
from util.httpClient import *
from config.config import *
from action.write_test_result import *
from action.check_result import *
def testInterface():
    parseE = ParseExcel()
    parseE.loadWorkBook(file_path)
    sheetObj = parseE.getSheetByName(u"API")
    activeList = parseE.getSingleColumn(sheetObj, API_ifExecute)
    for idx, cell in enumerate(activeList[1:], 2):
        if cell.value == 'y':
            rowObj = parseE.getSingleRow(sheetObj, idx)
            apiName = rowObj[API_apiName - 1].value
            requestUrl = rowObj[API_requestUrl - 1].value
            requestMethod = rowObj[API_requestMethod - 1].value
            paramsType = rowObj[API_paramsType - 1].value
            apiTestCaseFileName = rowObj[API_apiCaseSheetName - 1].value
            # print apiName,requestUrl,requestMethod,paramsType,apiTestCaseFileName
            # 下一步读sheet表，准备执行测试用例
            print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            print "apiTestCaseFileName:", apiTestCaseFileName
            caseSheetObj = parseE.getSheetByName(apiTestCaseFileName)
            caseActiveObj = parseE.getSingleColumn(caseSheetObj, CASE_ifExecute)
            for c_idx, col in enumerate(caseActiveObj[1:], 2):
                if col.value == 'y':
                    caseRowObj = parseE.getSingleRow(caseSheetObj, c_idx)
                    relyRule = caseRowObj[CASE_relyRule - 1].value
                    checkPoint=json.loads(caseRowObj[CASE_checkPoint-1].value)
                    print "relyRule:", relyRule

                    if relyRule:
                        # 发送接口请求之前，先获取请求数据
                        requestData = json.dumps(GetRequestData.getRequestData(eval(relyRule)))
                        print "requestData-2:", requestData
                    else:
                        requestData=caseRowObj[CASE_requestData-1].value
                        print "requestData without relyRule:",requestData,type(requestData)
                    hc = HttpClient()
                    print "requestMethod, requestUrl, paramsType, requestData:"
                    print requestMethod, requestUrl, paramsType, requestData
                    response = hc.request(requestMethod=requestMethod,
                                             requestUrl=requestUrl,
                                             paramsType=paramsType,
                                             requestData=requestData
                                             )
                    print "#############response.text##############:",response.text
                    if response.status_code ==200:
                        responseData=response.text
                        print "responseData-1,type(responsedata-1):",responseData,type(responseData)
                        errorKey=CheckResult.checkResult(json.loads(responseData),checkPoint)
                        write_result(parseE,caseSheetObj,c_idx,requestData=str(requestData),responseData=str(responseData),errorKey=errorKey)


                    else:
                        print "接口请求异常,状态码为：",response.status_code
                else:
                    print "接口用例被忽略执行"
        else:
            print "API测试被忽略"






if __name__ == "__main__":
    testInterface()
