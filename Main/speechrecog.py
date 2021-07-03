import requests
import io
def sendRequest():

    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles"

    headers = {
    "Content-Type" : "application/json",
    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }

    locale="en-us"
    # this was a file which was on my local machine so change it accordingly

    response = requests.request("POST",requestUrl,data=locale,headers = headers)
    return response

def getResponse(path,profileID):
    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles/{profileID}/enrollments"

    headers = {
    "Content-Type" : "audio/wav",

    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }
    body = open(path ,"rb").read()

    # this was a file which was on my local machine so change it accordingly

    response = requests.request("POST",requestUrl,headers = headers,data=body)
    return response

def identify(path,profileID):
    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles/{profileID}/verify"

    headers = {
    "Content-Type" : "audio/wav",
    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }

    # this was a file which was on my local machine so change it accordingly
    body = open(path ,"rb").read()
    response = requests.request("POST",requestUrl,headers = headers,data=body)
    return response