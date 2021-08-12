import os
from app import app, db
from models import Face, User
from forms import LoginForm
from flask import session, redirect, url_for, render_template, abort, request, flash, Response, send_from_directory
from flask_cors import CORS, cross_origin
import json
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import base64
from face_recogition import register_face, find_person
import requests

path="audio.wav"
profileID_dict={}


@app.route('/')
def index():
    return redirect(url_for('signup'))


@app.route('/dashboard')
def dashboard():
    user = User.get_by_username(session.get('username', None))
    return render_template("admin.html", balance=user.balance, username=user.username)

@app.route('/camera-in')
def camera_in():
    return render_template('camera_in.html')


@app.route('/camera-out')
def camera_out():
    return render_template('camera_out.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        user = User.get_by_username(username)
        if user and user.password == password:
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect(url_for('signup_id', user_id=new_user.id))
    return render_template('login.html', form=form)


@app.route('/signup/<user_id>', methods=['GET'])
def signup_id(user_id):
    if user_id not in profileID_dict:
        dosomething()
        profileID_dict[user_id]=profileID
        return render_template('voice.html', user_id=user_id)
    else:
        return render_template('index2.html', user_id=user_id)


@app.route('/signup-complete/<user_id>', methods=['GET','POST'])
def signup_complete(user_id):
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        for _ in range(3):
            verificationtrain()
        return render_template('index2.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/register', methods=['POST'])
def register_by_ui_path():
    name = request.form['name']
    image = request.files['photo']
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit()
    register_face([image.read()], new_user.username)

    return 'OK', 200


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/in', methods=['POST'])
def inputstream():
    if request.method == 'POST':
        file = request.files['webcam']
        if file:
            try:
                person_found = find_person(file.read())
                print(f'{person_found} checked in!')

            except:
                pass
            return 'OK', 200
        else:
            return 'NOT OK', 500


@app.route('/out', methods=['POST'])
def outputstream():
    if request.method == 'POST':
        file = request.files['webcam']
        if file:
            try:
                person_found = find_person(file.read())
                print(f'{person_found} checked out!')
                print('Total cost = Rs. 37')
                user = User.get_by_username(person_found)
                user.balance = user.balance - 37
                db.session.add(user)
                db.session.commit()
                print(f'New Balance: {user.balance}')
            except:
                pass
            return 'OK', 200
        else:
            return 'NOT OK', 500



def dosomething():
    response = sendRequest()
    json_data = json.loads(response.text)
    print(json_data['profileId'])
    global profileID
    profileID= json_data['profileId']

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