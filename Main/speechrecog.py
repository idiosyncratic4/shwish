import requests
import io
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS, cross_origin
import os
from subprocess import call, Popen, PIPE
import json


app = Flask(__name__)

@app.route('/home',methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def dosomething():
    response = sendRequest()
    json_data = json.loads(response.text)
    print(json_data['profileId'])
    return "abcd"



def sendRequest():

    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles/"

    headers = {
    "Content-Type" : "application/json",
    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }

    params = {
        'locale':'en-us'
    }
    # this was a file which was on my local machine so change it accordingly

    response = requests.request("POST",requestUrl,json=params,headers = headers)
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


if __name__ == '__main__':
    app.run(debug=True)