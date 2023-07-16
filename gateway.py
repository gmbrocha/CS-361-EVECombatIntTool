import json
from flask import Flask, jsonify, request, redirect, url_for, render_template
import requests

app = Flask(__name__)


# todo: add /<mail_type to route to create variable for conditional to set type of request from zkill svc


@app.route('/api/gateway/<pilot_name>/<mail_type>/<num_display>', methods=['GET'])
def gateway_service(pilot_name, mail_type, num_display):

    esi_svc_endpoint = f'http://localhost:5002/api/eve-esi-svc/{pilot_name}'
    esi_svc_resp = requests.post(esi_svc_endpoint)

    if esi_svc_resp.status_code == 200:
        resp = json.loads(esi_svc_resp.text)

        zkill_endpoint = f'http://localhost:5003/api/zkill-svc/{resp}/{mail_type}/{num_display}'
        zkill_svc_resp = requests.get(zkill_endpoint)
        if zkill_svc_resp.status_code == 200:
            response = json.loads(zkill_svc_resp.text)
            return jsonify(response)
        else:
            print("Error:", zkill_svc_resp.status_code)
            return

    else:
        print("Error:", esi_svc_resp.status_code)
        return


@app.route('/api/gateway-rand/<random_list>/<mail_type>/<num_display>', methods=['GET'])
def rand_gateway_service(random_list, mail_type, num_display):

    random_lst = json.loads(random_list)

    for rand in random_lst:
        zkill_endpoint = f'http://localhost:5003/api/zkill-svc/{rand}/{mail_type}/{num_display}'
        zkill_svc_resp = requests.get(zkill_endpoint)
        zkill_svc_json = json.loads(zkill_svc_resp.text)
        if len(zkill_svc_json) != 0:
            break

    if zkill_svc_resp.status_code == 200:
        response = json.loads(zkill_svc_resp.text)
        return jsonify(response)
    else:
        print("Error:", zkill_svc_resp.status_code)
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)