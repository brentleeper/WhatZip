from flask import *
from flask import jsonify
from dicttoxml import dicttoxml
from flask_cors import CORS, cross_origin
from get_postal_data import PostalDataDAO
import json
import traceback

valid_search_types = {'coordinate', 'radius', 'zipcode'}
valid_response_formats = {'json', 'xml'}
required_params = {
    'coordinate': {'lat', 'lon'},
    'radius': {'lat', 'lon', 'radius'},
    'zipcode': {'zipcode'}
}

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


def basic_response(user_token, _request, message, code, response_format, additional_data=None):
    response = {
            "user_token": user_token,
            "response_code": code,
            "message": message,
            "request_ip": _request.remote_addr,
            "request_params": _request.args
    }

    if additional_data and isinstance(additional_data, dict):
        for key in additional_data.keys():
            response.update({
                key: additional_data[key]
            })
    if response_format == "json":
        response = jsonify(response)
    elif response_format == "xml":
        response = dicttoxml(response).decode("utf-8")

    return response


def params_to_set(_request):
    param_set = set()
    for arg in request.args:
        param_set.add(arg)
    return param_set


def validate_params(search_type, _request):
    return len(required_params[search_type].difference(params_to_set(_request))) == 0


def validate_response_format(response_format):
    return response_format in valid_response_formats


def validate_search_type(search_type):
    return search_type in valid_search_types


def fulfill_request(user_token, search_type, response_format, _request):
    if not validate_search_type(search_type):
        return basic_response(
            user_token,
            _request,
            f"Bad Request: Invalid search_type '{search_type}' - Must use one of valid_search_types",
            400,
            response_format,
            {
                'valid_search_types': list(valid_search_types)
            }
        )

    if not validate_params(search_type, _request):
        return basic_response(
            user_token,
            _request,
            f"Bad Request: Missing required params",
            400,
            response_format,
            {
                'required_params': list(required_params[search_type])
            }
        )

    if not validate_response_format(response_format):
        return basic_response(
            user_token,
            _request,
            f"Bad Request: Invalid response_format '{response_format}' - Must use one of valid_response_formats",
            400,
            response_format,
            {
                'valid_response_formats': list(valid_response_formats)
            }
        )

    postal_dao = PostalDataDAO()

    if not postal_dao.conn:
        return basic_response(
            user_token,
            _request,
            f"Failed to connect to Database - Unreachable",
            503,
            response_format
        )

    if search_type in ["coordinate", "radius"]:
        lat = _request.args.get("lat")
        lon = _request.args.get("lon")

        valid_coords = postal_dao.validate_coordinates(float(lat), float(lon))
        if not all(valid_coords):
            bad_elements = []

            if not valid_coords[0]:
                bad_elements.append("'lat'")
            if not valid_coords[1]:
                bad_elements.append("'lon'")

            return basic_response(
                user_token,
                _request,
                f"Bad Request: Coordinate outside of valid range for: {','.join(bad_elements)}",
                400,
                response_format,
                {
                    "valid_range": {
                        "lat": "-90 <= lat <= 90",
                        "lon": "-180 <= lon <= 180"
                    }
                }
            )


    if search_type == "coordinate":
        results = postal_dao.get_data_from_coordinate(lat, lon)

    elif search_type == "radius":
        radius_miles = _request.args.get("radius")

        if not 0 < int(round(float(radius_miles))) <= 25:
            return basic_response(
                user_token,
                _request,
                f"Bad request: value for radius outside of allowed range",
                400,
                response_format,
                {
                    "valid_range": {
                        "radius": "0 < int(radius) <= 25"
                    }
                }
            )
        results = postal_dao.get_data_from_radius(lat, lon, radius_miles)

    elif search_type == 'zipcode':
        zipcode = _request.args.get("zipcode")
        results = postal_dao.get_data_from_zipcode(zipcode)

    if response_format == "json":
        for result in results:
            for key in result:
                if key == "geo_json":
                    result[key] = json.loads(result[key])

    return basic_response(user_token, _request, "success", 200, response_format, {'results': results, 'result_ct': len(results)})


@app.route('/<user_token>/<search_type>/<response_format>', methods=['GET'])
def main(user_token, search_type, response_format):
    auth = {'entication': True, 'orization': 'all'}  # to-do - implement auth

    if not auth['entication']:
        return basic_response(user_token, request, "forbidden - your access attempt has been logged", 403, response_format)

    fully_authorized = auth['orization'] == "all"

    if fully_authorized: #to-do: or get_authorization(auth['orization'], search_type, response_format)
        return fulfill_request(user_token, search_type, response_format, request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
