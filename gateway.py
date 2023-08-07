import json
from flask import Flask, jsonify, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/gateway/<pilot_name>/<mail_type>/<num_display>', methods=['GET'])
def gateway_service(pilot_name, mail_type, num_display):
    """
    Gateway route provides calls to 3 services - link_svc, zkill_svc and eve_esi_svc and builds a response object
    containing the pilot name and all relevant interaction data (# of kills/losses requested, ship type, pilot
    interacted with, modules fitted to loss) to be displayed in the app
    """
    # get char ID (int) from EVE ESI
    esi_svc_resp = requests.post(f'http://localhost:5002/eve-esi-svc/{pilot_name}')

    if esi_svc_resp.status_code == 200:
        # if pilot name returned valid char ID from ESI
        char_id = json.loads(esi_svc_resp.text)

        # this is just to grab character image and save to local directory temp for display
        get_char_avatar(char_id)

        # this is call to zkill api; response object also contains the call to partners link service
        zkill_svc_resp = requests.get(f'http://localhost:5003/zkill-svc/{char_id}/{mail_type}/{num_display}')
        response = normal_check_zkill_response_create_return_package(zkill_svc_resp, get_links(char_id))
        return jsonify(response)

    else:
        print("Error:", esi_svc_resp.status_code)
        return redirect(url_for('get_pilot'))


@app.route('/gateway-rand/<random_list>/<mail_type>/<num_display>', methods=['GET'])
def rand_gateway_service(random_list, mail_type, num_display):
    """Gateway route provides calls to 3 services - link_svc, zkill_svc and eve_esi_svc and builds a response object
    containing the pilot name and all relevant interaction data (# of kills/losses requested, ship type, pilot
    interacted with, modules fitted to loss) to be displayed in the app"""

    # get the zkill response package and char id from make_random_calls
    zkill_svc_resp, char_id = make_random_calls(json.loads(random_list), mail_type, num_display)

    # get char name
    char_name = get_char_name(char_id)

    # get char avatar
    get_char_avatar(char_id)

    # this is call to zkill api; response object also contains the call to partners link service
    response = random_check_zkill_response_create_return_package(zkill_svc_resp, char_name, get_links(char_id))
    return jsonify(response)


def get_char_name(char_id):
    """
    Accepts int as single argument and returns the str character name from the call to ESI svc
    """
    esi_svc_resp = requests.get(f'http://localhost:5002/eve-esi-svc/{char_id}')

    if esi_svc_resp.status_code == 200:
        return json.loads(esi_svc_resp.text)
    else:
        return None


def get_links(char_id):
    """
    Makes call to link_svc to get the 2 link json package for the response object
    """
    link_resp = requests.get(f'http://localhost:5004/link-svc/{char_id}')
    return link_resp


def make_random_calls(random_list: list, mail_type: str, num_display: int):
    """
    Accepts a list of random ints (valid charIDs) and makes calls for each in a loop until a valid, non-empty response
    is given, each of the calls contains the
    """
    for char_id in random_list:
        zkill_svc_resp = requests.get(f'http://localhost:5003/zkill-svc/{char_id}/{mail_type}/{num_display}')
        zkill_svc_json = json.loads(zkill_svc_resp.text)
        # if response object is not empty (will return empty dicts if not valid) then return that object and the id
        if len(zkill_svc_json) != 0:
            return zkill_svc_resp, char_id


def random_check_zkill_response_create_return_package(zkill_svc_resp, charName: str, link_resp):
    """
    Accepts 2 response (from 2 separate API calls) objects and a single str (charName), checks the first response
    (zkill) status and if good response packages the str and de-jsoned link object together with that first response
    and returns to the app; if bad response from the zkill redirect to index/get_pilot
    """
    if zkill_svc_resp.status_code == 200:
        response = json.loads(zkill_svc_resp.text)
        response["charName"] = charName
        links = json.loads(link_resp.text)
        response["links"] = links
        return response
    else:
        print("Error:", zkill_svc_resp.status_code)
        return redirect(url_for('get_pilot'))


def normal_check_zkill_response_create_return_package(zkill_svc_resp, links):
    """
    Accepts 2 response objects, checks the zkill response status and if good - builds package with the de-jsoned link
    object and returns to app; if bad response redirect to index/get_pilot
    """
    if zkill_svc_resp.status_code == 200:
        response = json.loads(zkill_svc_resp.text)
        links = json.loads(links.text)  # send this in the json package also
        response["links"] = links
        return response
    else:
        print("Error:", zkill_svc_resp.status_code)
        return redirect(url_for('get_pilot'))


def get_char_avatar(char_id):
    """
    Accepts single argument int and request avatar from evetech, store locally for display; returns nothing
    """
    char_img_req = requests.get(f'https://images.evetech.net/characters/{char_id}/portrait?size=64')

    if char_img_req.status_code == 200:  # save image to local directory
        with open('static/images/char-img.png', 'wb') as file:
            file.write(char_img_req.content)
    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)