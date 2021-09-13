from flask import Flask
from flask import render_template, Response, request,flash
from flask.helpers import url_for
from flask_mail import Mail, Message
import subprocess
import platform
import cv2 as cv
import os

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get("API_KEY")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("DEFAULT")
mail = Mail(app)

def send_mail(cam):
    recipient = "testnode13@gmail.com"
    msg = Message('Non Working Camera Information', recipients=[recipient])

    txt="Non working camera: "+cam
    msg.body = (txt)
    msg.html="<b>"+txt+"</b>"
    mail.send(msg)
    


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for th-e number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else 'c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


def genFrames(cameraNum):
    cameraNum -= 1
    videoFeed = cv.VideoCapture(cameraNum)
    while True:
        isReceiving, frame = videoFeed.read()
        if not isReceiving:
            break
        else:
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/status')
def status():

    count = 0
    hosts = ["google.com", "asdfasdf.com"]
    working = ""
    notWorking = ""
    for host in hosts:
        count += 1
        if(ping(host)):
            working += '<a href="camera?camera=' + \
                str(count) + '"<div class="card">' + host + '</div></a>'
        else:
            send_mail(host)
            notWorking += '<div class="card">' + host + '</div>'

    return render_template('status.html', Work=working, Nwork=notWorking)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/camera')
def camera():
    return render_template('camera.html', cameraNum=request.args.get("camera"))


@app.route('/video_feed')
def video_feed():
    cameraNum = int(request.args.get("camera"))
    return Response(genFrames(cameraNum), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/cya")
def cya():
    return "Does nothing"


if __name__ == '__main__':
    app.run(debug=True)
