from flask import Flask
import os
import signal

app = Flask(__name__)

@app.route('/')
def home():
    return "I am alive", 200

@app.route('/crash')
def crash():
    print("Crashing now")
    os._exit(1)
    return "Crashing..", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)