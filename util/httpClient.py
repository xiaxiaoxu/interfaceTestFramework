#encoding=utf-8
import requests
import json
class HttpClient(object):
    def __init__(self):
        pass

    def __post(self,url,data=None,json=None,**kargs):
        response=requests.post(url=url,data=data,json=json)
        return response

    def __get(self,url,params=None,**kargs):
        response=requests.get(url=url,params=params)


    def request(self,requestMethod,requestUrl,paramsType,requestData=None,headers=None,cookies=None):
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response=self.__post(url=requestUrl,data=json.dumps(eval(requestData)),headers=headers,cookies=cookies)
                return response
            elif paramsType == 'json':
                response = self.__post(url=requestUrl,json=json.dumps(eval(requestData)),headers=headers,cookies=cookies)
                return response
        elif requestMethod == "get":
            if paramsType == "url":
                request_url="%s%s" %(requestUrl,requestData)
                response=self.__get(url=request_url,headers=headers,cookies=cookies)
                return response
            elif paramsType == "params":
                response=self.__get(url=requestUrl,params=requestData,headers=headers,cookies=cookies)
                return response

if __name__ == "__main__":
    hc=HttpClient()
    response=hc.request("post","http://39.106.41.11:8080/register/","form",'{"username":"xufengchai6","password":"xufengchai121","email":"xufengchai@qq.com"}')
    print response.text

