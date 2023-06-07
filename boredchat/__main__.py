from . import app, create, DIR
from gevent import monkey
from gevent.pywsgi import WSGIServer
import os


def main():
    monkey.patch_all()
    SECRET = os.path.join(DIR, "secret.key")
    if os.path.isfile(SECRET):
        with open(SECRET) as f:
            secret = f.readline()[:-1] #read 1st line, no trailing newline char
    else:
        secret = input("Enter secret: ")
        with open(SECRET, "w") as f:
            f.write(secret)
    app.secret_key = secret

    create()
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()

if __name__ == "__main__":
    main()