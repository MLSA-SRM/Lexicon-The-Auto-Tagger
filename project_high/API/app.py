from flask import Flask
import time

app = Flask(__name__)

# train initial
x = 0
for x in range(0, 1000):
    x += 1

# routes
@app.route('/')
def hello_world():
    return str(x)

@app.rout('/check_tag')
def check_tag():
    