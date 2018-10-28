#encoding=utf-8
from config import * 
from util.ParseExcel import *
from action.getRequestData import *
import json

def write_result(wbObj,sheetObj,rowNum,requestData=None,responseData=None,errorKey = None):
    try:
        if requestData:
            #写入请求数据
            print "requestData-4:",requestData
            print "type(requestData-4):",type(requestData)

            wbObj.writeCell(sheet=sheetObj,content=requestData,rowNo=rowNum,colNo=CASE_requestData)
        if responseData:
            #写响应body
            wbObj.writeCell(sheet=sheetObj,content=responseData,rowNo=rowNum,colNo=CASE_responseData)
        #写校验结果状态列及错误信息列
        if errorKey:
            wbObj.writeCell(sheet=sheetObj,content="failed",rowNo=rowNum,colNo=CASE_result)
            wbObj.writeCell(sheet=sheetObj,content="%s" %errorKey,rowNo = rowNum,colNo=CASE_errorInfo)
        else:
            wbObj.writeCell(sheetObj,content="pass",rowNo=rowNum,colNo=CASE_result)
    except Exception,e:
        raise e

        
if __name__ == "__main__":
    parseE=ParseExcel()
    parseE.loadWorkBook(file_path)
    sheetObj=parseE.getSheetByName(u"API")
    activeList=parseE.getSingleColumn(sheetObj,API_ifExecute)
    for idx,cell in enumerate(activeList[1:],2):
        if cell.value == 'y':
            rowObj=parseE.getSingleRow(sheetObj,idx)
            apiName=rowObj[API_apiName-1].value
            requestUrl=rowObj[API_requestUrl-1].value
            requestMethod = rowObj[API_requestMethod-1].value
            paramsType = rowObj[API_paramsType-1].value
            apiTestCaseFileName=rowObj[API_apiCaseSheetName-1].value
            #print apiName,requestUrl,requestMethod,paramsType,apiTestCaseFileName
            #下一步读sheet表，准备执行测试用例
            print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            print "apiTestCaseFileName:",apiTestCaseFileName
            caseSheetObj=parseE.getSheetByName(apiTestCaseFileName)
            caseActiveObj=parseE.getSingleColumn(caseSheetObj,CASE_ifExecute)
            for c_idx,col in enumerate(caseActiveObj[1:],2):
                if col.value == 'y':
                    caseRowObj=parseE.getSingleRow(caseSheetObj,c_idx)
                    relyRule=caseRowObj[CASE_relyRule-1].value
                    print "relyRule:",relyRule
                    if relyRule:
                        #发送接口请求之前，先获取请求数据
                        requestData=json.dumps(GetRequestData.getRequestData(eval(relyRule)))
                        print "requestData-2:",requestData
                        #write_result(parseE,caseSheetObj,c_idx,requestData=requestData)
                        #print "print requestData Done!"

                        






















































