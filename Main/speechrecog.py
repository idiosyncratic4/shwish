import requests
import io
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS, cross_origin
import os
from subprocess import call, Popen, PIPE
import json
import wave

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)