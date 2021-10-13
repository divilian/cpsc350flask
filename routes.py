
from flask import render_template
from flask import request
from fallbreak import bj
import sqlite3


@bj.route("/showrecipe")
def showrecipe():
    conn = sqlite3.connect("/home/stephen/teaching/350/bj.sqlite")
    cur = conn.cursor()
    if "numcartons" in request.args:
        cur.execute(    
        """
        update recipe set cartonsOrdered=cartonsOrdered+?
        where name=?
        """, (int(request.args['numcartons']), request.args['recipe'])
        )
        conn.commit()
        return ("Nathan was right! " +
            f"You have now ordered {request.args['numcartons']} cartons of " +
            f"{request.args['recipe']}")
    else:
        recipename = request.args["recipe"]
        stephen = cur.execute(
            """
            select mixin_name, costPerOz from ingredients, mixin
            where ingredients.mixin_name = mixin.name
            and recipe_name=?
            """, (request.args["recipe"],)).fetchall()
        return render_template("showrecipe.html",
            recipe=request.args["recipe"], mixins=stephen)
 

@bj.route("/")
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
