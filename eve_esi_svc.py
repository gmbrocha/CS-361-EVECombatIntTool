import json
from flask import Flask, jsonify, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/api/eve-esi-svc/<pilotName>', methods=['POST'])
def eve_esi_svc(pilotName):

    ids_endpoint = f"https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en"
    payload = [pilotName]
    esi_resp = requests.post(ids_endpoint, json=payload)

    if esi_resp.status_code == 200:
        resp = json.loads(esi_resp.text)
        charID = resp["characters"][0]["id"]
        return jsonify(charID)
    else:
        print("Error:", esi_resp.status_code)
        return


@app.route('/api/eve-esi-svc/<charID>', methods=['GET'])
def eve_esi_svc_name(charID):

    ids_endpoint = f"https://esi.evetech.net/latest/characters/{charID}/?datasource=tranquility"
    esi_resp = requests.get(ids_endpoint)

    if esi_resp.status_code == 200:
        resp = json.loads(esi_resp.text)
        charName = resp["name"]
        return jsonify(charName)
    else:
        print("Error:", esi_resp.status_code)
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)