import requests
import io
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS, cross_origin
import os
from subprocess import call, Popen, PIPE
import json
import wave

app = Flask(__name__)
#profileID="4d1cfca2-4249-41f7-8102-9f11fd692d48"
path="uploads/record.wav"

@app.route('/home',methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def dosomething():
    response = sendRequest()
    json_data = json.loads(response.text)
    print(json_data['profileId'])
    global profileID
    profileID= json_data['profileId']
    return "abcd"

@app.route('/verify',methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def verificationtrain():
    response = getResponse(path,profileID)
    json_data = json.loads(response.text)
    print(json_data)
    return "abcd"

@app.route('/identify',methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def identification():
    response = identify(path,profileID)
    json_data = json.loads(response.text)
    print(json_data)
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
    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles/{0}/enrollments"

    headers = {
    "Content-Type" : "audio/wav",
    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }
    w = open(path, 'rb')
    # binary_data = w.readframes(w.getnframes())

    print(profileID)
    # this was a file which was on my local machine so change it accordingly

    response = requests.request("POST",requestUrl.format(profileID),data=w,headers = headers)
    return response


def identify(path,profileID):
    requestUrl = "https://westus.api.cognitive.microsoft.com/speaker/verification/v2.0/text-dependent/profiles/{0}/verify"

    headers =  {
    "Content-Type" : "audio/wav",
    "Ocp-Apim-Subscription-Key" : "fe29f57488b04a81a330347d50b1a599",
    }

    # this was a file which was on my local machine so change it accordingly
    w = open(path, 'rb')

    response = requests.request("POST",requestUrl.format(profileID),data=w,headers = headers)
    return response


if __name__ == '__main__':
    app.run(debug=True)