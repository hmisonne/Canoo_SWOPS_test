from flask import Flask
from flask import render_template, abort, redirect, url_for, request, jsonify
from flask_cors import CORS
import json
import uuid

app = Flask(__name__)
CORS(app)

# Configure "database" as json file
database_path = "data.json"
app.config['JSON_DATA'] = database_path


def read_json():
    path = app.config["JSON_DATA"]
    with open(path) as jsonFile:
        return json.load(jsonFile)


def write_json(data):
    path = app.config["JSON_DATA"]
    with open(path, "w") as jsonFile:
        json.dump(data, jsonFile)


@app.route("/temperature", methods=['GET'])
def get_temperature():
    try:
        data = read_json()
        result = data['temperature']
        response = {
                'success': True,
                'data': result
        }
        app.logger.info('%s %s %s',request.method, request.url_rule, response)
        return jsonify(response)
       
    except:
        app.logger.info('%s %s %s',request.method, request.url_rule, "422: unprocessable")
        abort(422)

@app.route("/temperature", methods=[ 'POST'])
def set_temperature():
    body = request.get_json()
    value = body.get('temperature', None)
    if value is None or type(value) != int:
        app.logger.error('%s %s %s',request.method, request.url_rule, "400: Bad request")
        abort(400)
    data = read_json()
    data["temperature"] = value
    write_json(data)
    response = {
        'success': True,
        'data': value
    }
    app.logger.info('%s %s %s',request.method, request.url_rule, response)
    return jsonify(response)


@app.route("/lights", methods=["GET"])
def get_lights():
    try:
        data = read_json()
        result = list(data['lights'].values())
        response = {
            'success': True,
            'data': result
        }
        app.logger.info('%s %s %s',request.method, request.url_rule, response)
        return jsonify(response)
    except:
        app.logger.info('%s %s %s',request.method, request.url_rule, "422: unprocessable")
        abort(422)

@app.route("/lights", methods=["POST"])
def add_light():
    try:
        data = read_json()
        light_id = uuid.uuid1().hex
        newLight = {
            "id": light_id,
            "turnedOn": False,
        }

        data["lights"][light_id] = newLight
        write_json(data)
        response = {
            'success': True,
            'data': newLight
        }
        
        app.logger.info('%s %s %s',request.method, request.url_rule, response)
        return jsonify(response)
    except:
        app.logger.info('%s %s %s',request.method, request.url_rule, "422: unprocessable")
        abort(422)

@app.route("/lights/<light_id>", methods=["GET"])
def get_light(light_id):
    data = read_json()
    light = data["lights"].get(light_id, None)
    if light is None:
        app.logger.error('%s %s=%s %s',request.method, request.url_rule, light_id, "404: Resource not found")
        abort(404)
    response = {
        'success': True,
        'data': light
    }
    
    app.logger.info('%s %s=%s %s',request.method, request.url_rule, light_id, response)
    return jsonify(response)


@app.route("/lights/<light_id>", methods=["DELETE"])
def remove_light(light_id):
    data = read_json()
    light_toDelete = data["lights"].get(light_id, None)
    if light_toDelete is None:
        app.logger.error('%s %s=%s %s',request.method, request.url_rule, light_id, "404: Resource not found")
        abort(404)
    del data["lights"][light_id]
    write_json(data)

    response = {
        'success': True,
        'light_deleted': light_id
    }
    app.logger.info('%s %s=%s %s',request.method, request.url_rule, light_id, response)
    return jsonify(response)



@app.route("/lights/<light_id>", methods=["PUT"])
def toggle_light(light_id):
    data = read_json()
    light_toToggle = data["lights"].get(light_id, None)
    if light_toToggle is None:
        app.logger.error('%s %s=%s %s',request.method, request.url_rule, light_id, "404: Resource not found")
        abort(404)
    light_toToggle['turnedOn'] = not light_toToggle['turnedOn']
    write_json(data)

    response = {
        'success': True,
        'data': light_toToggle
    }
    
    app.logger.info('%s %s=%s %s',request.method, request.url_rule, light_id, response)
    return jsonify(response)


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
        }), 400