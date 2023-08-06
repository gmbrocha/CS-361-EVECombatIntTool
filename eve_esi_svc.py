import json
from flask import Flask, jsonify, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/eve-esi-svc/<pilot_name>', methods=['POST'])
def eve_esi_svc(pilot_name):
    """
    Service route receives a character name str, makes a request with it to EVE ESI, and responds to request with the
    int charID associated with
    """
    esi_resp = requests.post(
        f"https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        json=[pilot_name]
    )

    # check ESI response status and respond to local request accordingly
    if esi_resp.status_code == 200:
        resp = json.loads(esi_resp.text)
        # get charID from the response and send back to request
        return jsonify(resp["characters"][0]["id"])
    else:
        print("Error:", esi_resp.status_code)
        return redirect(url_for('get_pilot'))


@app.route('/eve-esi-svc/<charID>', methods=['GET'])
def eve_esi_svc_name(charID):
    """
    Service route receives a character ID, makes a request with it to EVE ESI, and responds to request with the name
    associated with
    """
    esi_resp = requests.get(
        f"https://esi.evetech.net/latest/characters/{charID}/?datasource=tranquility"
    )

    # check ESI response status and respond to local request accordingly
    if esi_resp.status_code == 200:
        resp = json.loads(esi_resp.text)
        # get name value from the response and send back to request
        return jsonify(resp["name"])
    else:
        print("Error:", esi_resp.status_code)
        return redirect(url_for('get_pilot'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)