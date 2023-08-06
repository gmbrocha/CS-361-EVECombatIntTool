import json
from flask import Flask, jsonify, request, redirect, url_for, render_template
import requests

app = Flask(__name__)


@app.route('/api/gateway/<pilot_name>/<mail_type>/<num_display>', methods=['GET'])
def gateway_service(pilot_name, mail_type, num_display):

    # get char ID (int) from EVE ESI
    esi_svc_endpoint = f'http://localhost:5002/api/eve-esi-svc/{pilot_name}'
    esi_svc_resp = requests.post(esi_svc_endpoint)

    # if pilot name returned valid char ID from ESI
    if esi_svc_resp.status_code == 200:
        resp = json.loads(esi_svc_resp.text)

        # this is the call to your service
        link_endpoint = f'http://localhost:5004/api/link-svc/{resp}'
        link_resp = requests.get(link_endpoint)

        zkill_endpoint = f'http://localhost:5003/zkill-svc/{resp}/{mail_type}/{num_display}'
        zkill_svc_resp = requests.get(zkill_endpoint)

        char_img_endpoint = f'https://images.evetech.net/characters/{resp}/portrait?size=64'
        char_img_req = requests.get(char_img_endpoint)

        if char_img_req.status_code == 200:  # save image to local directory
            with open('static/images/char-img.png', 'wb') as file:
                file.write(char_img_req.content)

        if zkill_svc_resp.status_code == 200:
            response = json.loads(zkill_svc_resp.text)
            links = json.loads(link_resp.text)  # send this in the json package also
            response["links"] = links
            return jsonify(response)
        else:
            print("Error:", zkill_svc_resp.status_code)
            return redirect(url_for('get_pilot'))

    else:
        print("Error:", esi_svc_resp.status_code)
        return redirect(url_for('get_pilot'))


@app.route('/api/gateway-rand/<random_list>/<mail_type>/<num_display>', methods=['GET'])
def rand_gateway_service(random_list, mail_type, num_display):

    random_list = json.loads(random_list)

    zkill_svc_resp, rand = make_random_calls(random_list, mail_type, num_display)

    # get char name
    esi_svc_endpoint = f'http://localhost:5002/api/eve-esi-svc/{rand}'
    esi_svc_resp = requests.get(esi_svc_endpoint)

    if esi_svc_resp.status_code == 200:
        charName = json.loads(esi_svc_resp.text)
    else:
        charName = None

    # call to partners link svc
    link_endpoint = f'http://localhost:5004/api/link-svc/{rand}'
    link_resp = requests.get(link_endpoint)

    # get char avatar
    char_img_endpoint = f'https://images.evetech.net/characters/{rand}/portrait?size=64'
    char_img_req = requests.get(char_img_endpoint)

    if char_img_req.status_code == 200:  # save image to local directory
        with open('static/images/char-img.png', 'wb') as file:
            file.write(char_img_req.content)

    if zkill_svc_resp.status_code == 200:
        response = json.loads(zkill_svc_resp.text)
        response["charName"] = charName
        links = json.loads(link_resp.text)
        response["links"] = links
        return jsonify(response)
    else:
        print("Error:", zkill_svc_resp.status_code)
        return redirect(url_for('get_pilot'))


def make_random_calls(random_list: list, mail_type: str, num_display: int):
    for rand in random_list:
        zkill_endpoint = f'http://localhost:5003/zkill-svc/{rand}/{mail_type}/{num_display}'
        zkill_svc_resp = requests.get(zkill_endpoint)
        zkill_svc_json = json.loads(zkill_svc_resp.text)
        if len(zkill_svc_json) != 0:
            return zkill_svc_resp, rand


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)