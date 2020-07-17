from pprint import pprint

from flask import Flask, render_template, request, redirect
from io import StringIO  # Python3
import sys
import yaml
import base64

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return redirect(
        "/information/eWFtbDogVGhlIGluZm9ybWF0aW9uIHBhZ2UgaXMgc3RpbGwgdW5kZXIgY29uc3RydWN0aW9uLCB1cGRhdGVzIGNvbWluZyBzb29uIQ==",
        code=302)


@app.route("/information/<input>", methods=['GET'])
def deserialization(input):
    try:
        if not input:
            return render_template("information/index.html")
        yaml_file = base64.b64decode(input)
        content = yaml.safe_load(yaml_file)
        pprint(content)
    except Exception as err:
        return "The application was unable to  to deserialize the object!: " + err.__str__()
    return render_template("index.html", content=content['yaml'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
