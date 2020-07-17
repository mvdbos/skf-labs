import builtins
import hashlib
import hmac
import io
import pickle, sys, yaml
from io import StringIO  # Python3
from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

safe_builtins = {
    'range',
    'complex',
    'set',
    'frozenset',
    'slice',
}


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()


@app.route("/")
def start():
    user = {'name': 'ZeroCool'}
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(user, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('filename.pickle', 'rb') as handle:
        a = pickle.load(handle)
    return render_template("index.html", content=a)


@app.route("/sync", methods=['POST'])
def deserialization():
    received_data = request.form['data_obj']
    received_digest, pickled_hexdata = received_data.split(' ')
    pickled_data = bytes.fromhex(pickled_hexdata)

    computed_digest = hmac.new(b'shared-key', pickled_data, hashlib.sha256).hexdigest()
    if received_digest != computed_digest:
        return render_template("index.html", content='Integrity check failed')
    else:
        a = restricted_loads(pickled_data)

    # a = pickle.loads(attack)

    # with open("pickle.hacker", "wb+") as file:
    #     att = request.form['data_obj']
    #     attack = bytes.fromhex(att)
    #     file.write(attack)
    #     file.close()
    # with open('pickle.hacker', 'rb') as handle:
    #     a = pickle.load(handle)
    #     print(attack)
    return render_template("index.html", content=a)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
