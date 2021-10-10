
from flask import render_template
from flask import request
from fallbreak import bj
import sqlite3

@bj.route("/")
@bj.route("/haveagreatbreak")
def saraid():
    return "Have a <i><b>good</b></i> one too!"

@bj.route("/showrecipe")
def showrecipe():
    recipename = request.args["recipe"]
    conn = sqlite3.connect("/home/stephen/teaching/350/bj.sqlite")
    cur = conn.cursor()
    stephen = cur.execute(
        """
        select mixin_name from ingredients where recipe_name=?
        """, (request.args["recipe"],)).fetchall()
    return render_template("showrecipe.html",
        recipe=request.args["recipe"], mixins=stephen)
    

@bj.route("/chooseflavor")
def chooseflavor():
    conn = sqlite3.connect("/home/stephen/teaching/350/bj.sqlite")
    cur = conn.cursor()
    if "chooseflavor" in request.args:
        brian = cur.execute(
            """
            select name, cartonsOrdered from recipe where flavorName=?
            """, (request.args["chooseflavor"],)).fetchall()
        if len(brian) == 0:
            return f"No recipes with {request.args['chooseflavor']}, bub!"
        return render_template("browserecipes.html",
            faveFlave=request.args["chooseflavor"], recipes=brian)
    else:
        jd = cur.execute("select name from flavor").fetchall()
        return render_template("chooseflavor.html", flavors=jd)
