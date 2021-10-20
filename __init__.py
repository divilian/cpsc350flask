
from flask import Flask
bj = Flask(__name__)
from cpsc350flask import routes

bj.secret_key = "I love tunafish!"
