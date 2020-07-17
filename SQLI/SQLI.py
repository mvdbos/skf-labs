from pprint import pprint

from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, abort

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/home/<pageId>", methods=['GET'])
def inject(pageId):
    # if (pageId.isnumeric()):
    if pageId == 0:
        pageId = 1
    sqli = Pages()
    pprint(pageId)
    values = sqli.getPage(pageId)
    pprint(values)
    id = values[0][0]
    title = values[0][1]
    content = values[0][2]
    return render_template("index.html", title=title, content=content, id=id)


# else:
#    abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# UNION SELECT 1,username,password FROM users
