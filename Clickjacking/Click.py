from flask import Flask, request, url_for, render_template, redirect, make_response


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    r = make_response(render_template('index.html'))
    r.headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self'; frame-ancestors 'self';")
    r.headers.set('X-Frame-Options', "SAMEORIGIN")
    return r

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
