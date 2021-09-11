from flask import Flask
from flask import render_template
from flask.helpers import url_for
import subprocess
import platform
app = Flask(__name__)

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for th-e number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else 'c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/status')
def status():

   hosts = ["google.com", "asdfasdf.com"]
   working = ""
   notWorking = ""
   for host in hosts:
      if(ping(host)):
         working += '<div class="card">' + host + '</div>'
      else:
         notWorking += '<div class="card">' + host + '</div>'
         
   return render_template('status.html', Work=working, Nwork=notWorking)


@app.route('/main')
def main():
   return render_template('main.html')

@app.route("/cya")
def cya():
   return "Does nothing"

if __name__ == '__main__':
   app.run(debug = True)