import flask
import json


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/cars', methods=['GET', 'POST'])
def cars():
    with open('vint.json', 'r') as file:
        file = json.loads(file.read())
    if flask.request.method == 'GET':
        if (arg := flask.request.args):
            if (argv := arg.get('sort')):
                file['cars'].sort(
                        key=lambda x: x[argv],
                        reverse=arg.get('order') == 'desc')
    if flask.request.method == 'POST':
        data = flask.request.json
        file['cars'].append(data)
        with open('vint.json', 'w') as new:
            new.write(json.dumps(file))
        return flask.Response(file, status=201)
    return file


@app.route('/cars/<arg>', methods=['GET', 'PUT', 'DELETE'])
def cars_id(arg=None):
    with open('vint.json', 'r') as file:
        file = json.loads(file.read())
    for car in file.get('cars'):
        if str(car['id']) == arg:
            if flask.request.method == 'GET':
                return car
            elif flask.request.method == 'DELETE':
                file['cars'].remove(car)
                with open('vint.json', 'w') as new:
                    new.write(json.dumps(file))
                return file
            elif flask.request.method == 'PUT':
                file['cars'].remove(car)
                data = flask.request.json
                file['cars'].insert(data['id']-1, data)
                with open('vint.json', 'w') as new:
                    new.write(json.dumps(file))
                return file
    else:
        return flask.Response(status=404)


if __name__ == "__main__":
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    app.run(debug=True)
