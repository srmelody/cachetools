from functools import wraps

from flask import make_response
from flask import Flask
from flask import request, Response


from OpenSSL import SSL

app = Flask(__name__)

users = {'admin': 'secret', 'user': 'user'}


@app.before_request
def before_request():
    print request.headers


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    passwd = users[username]
    return passwd == password

    #return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/secure")
@requires_auth
def secure():
    return "Secured resource"


@app.route("/api/admin")
@requires_auth
def admin():
    if request.authorization and request.authorization.username == 'admin':
        response = make_response("Secured resource", 200)
        response.cache_control.private = True
        return response
    else:
        return make_response("Verboten!", 403)


@app.route("/api/same")
def same():
    return "I always return hello world!"


@app.route("/api/user")
def user():
    if request.authorization and request.authorization.username:
        response = make_response(request.authorization.username, 200)
        response.cache_control.private = True
        return response
    else:
        return "No user"


if __name__ == "__main__":
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('/etc/ssl/localhost/server.key')
    context.use_certificate_file('/etc/ssl/localhost/server.cert')
    app.run("127.0.0.1", 8080, debug=True, ssl_context=context)

