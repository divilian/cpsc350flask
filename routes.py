
from flask import render_template
from flask import request, redirect, url_for, session
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
        if 'orders' not in session:
            session['orders'] = []
        session['orders'].append((request.args['recipe'],
            request.args['numcartons']))
        session.modified = True

        stephen = cur.execute(
            """
            select mixin_name, costPerOz from ingredients, mixin
            where ingredients.mixin_name = mixin.name
            and recipe_name=?
            """, (request.args["recipe"],)).fetchall()
        return render_template("showrecipe.html",
            recipe=request.args["recipe"], mixins=stephen,
            msg=f"Thanks for your {request.args['numcartons']}-carton " +
                f"order of {request.args['recipe']}!",
                orders=session['orders'])
    else:
        recipename = request.args["recipe"]
        stephen = cur.execute(
            """
            select mixin_name, costPerOz from ingredients, mixin
            where ingredients.mixin_name = mixin.name
            and recipe_name=?
            """, (request.args["recipe"],)).fetchall()
        return render_template("showrecipe.html",
            recipe=request.args["recipe"], mixins=stephen,
            orders=session['orders'] if 'orders' in session else [])
 
@bj.route("/browserecipes")
def browserecipes():
    conn = sqlite3.connect("/home/stephen/teaching/350/bj.sqlite")
    cur = conn.cursor()
    brian = cur.execute(
        """
        select name, cartonsOrdered from recipe where flavorName=?
        """, (request.args["chooseflavor"],)).fetchall()
    if len(brian) == 0:
        return f"No recipes with {request.args['chooseflavor']}, bub!"
    return render_template("browserecipes.html",
        faveFlave=request.args["chooseflavor"], recipes=brian,
        orders=session['orders'] if 'orders' in session else [])

@bj.route("/")
@bj.route("/chooseflavor")
def chooseflavor():
    conn = sqlite3.connect("/home/stephen/teaching/350/bj.sqlite")
    cur = conn.cursor()
    if "chooseflavor" in request.args:
        return redirect(url_for("browserecipes",
            chooseflavor=request.args['chooseflavor']))
    else:
        jd = cur.execute("select name from flavor").fetchall()
        return render_template("chooseflavor.html", flavors=jd,
            orders=session['orders'] if 'orders' in session else [])
