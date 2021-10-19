
from flask import Flask
bj = Flask(__name__)
from fallbreak import routes

bj.secret_key = "I love tunafish!"
