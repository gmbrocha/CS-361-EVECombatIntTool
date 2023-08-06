import json
from flask import Flask, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/zkill-svc/<charID>/<mail_type>/<num_display>', methods=['GET'])
def zkill_svc(charID, mail_type, num_display):
    """
    """
    # request at the endpoint for the zkill API with either kills/losses, and character ID int range (90000000-98000000)
    response = requests.get(f"https://zkillboard.com/api/{mail_type}/characterID/{charID}/")

    if response.status_code == 200:
        # generate list of dicts for each kill id associated with the charID
        ids_dicts = create_dict_list_from_killids_response(response, num_display)

        # generate dict of killmails and return to call
        allmails = create_allmails_dict(ids_dicts) # pass list of dicts (from
        return jsonify(allmails)
    else:
        print(f'Error {response.status_code}')
        return redirect(url_for('get_pilot'))


def create_allmails_dict(ids):
    """
    """
    allmails = {}
    for idx in ids:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 + '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                   }
        # make requests for each kill id, and parse that into kill_info below
        response = requests.get('https://zkillboard.com/kill/' + str(idx) + '/', headers=headers)

        # use BS to parse the zkill endpoint html into str
        kill_info = BeautifulSoup(response.text, 'html.parser')
        # this will be the 'header info' for each kill - kill id, ship, pilot name, and all modules fitted
        kill_info_list = create_kill_header_info(kill_info)

        # for each individual loss/kill (for the character associated w/ charID) set value at the 'kill id' key
        allmails[idx] = create_joined_info(kill_info, kill_info_list)
    return allmails


def create_kill_header_info(kill_info):
    """
    """
    title = kill_info.title
    title_to_list = str(title.text).split("|")
    kill_info_list = []
    for i in range(3):
        kill_info_list.append(title_to_list[i].strip())
    return kill_info_list


def create_joined_info(kill_info, kill_info_list):
    """
    """
    fittings_highs, fittings_mids, fittings_lows = [], [], []
    for i in range(1, 9):
        # parse the beautiful soup html for high, mid, low -- this will then become a string of all the modules for each
        highs, mids, lows = kill_info.find("div", {"id": f"high{i}"}), kill_info.find("div", {"id": f"mid{i}"}), \
            kill_info.find("div", {"id": f"low{i}"})
        highs, mids, lows = str(highs), str(mids), str(lows)

        # parse each str (highs, mids, lows) for indices to slice and append to appropriate fittings_list
        start_idx = highs.find("title")
        if start_idx != -1:
            end_idx = highs.index('"', start_idx + 7)
            fittings_highs.append(highs[(start_idx + 7):end_idx])

        start_idx = mids.find("title")
        if start_idx != -1:
            end_idx = mids.index('"', start_idx + 7)
            fittings_mids.append(mids[(start_idx + 7):end_idx])

        start_idx = lows.find("title")
        if start_idx != -1:
            end_idx = lows.index('"', start_idx + 7)
            fittings_lows.append(lows[(start_idx + 7):end_idx])

    # combine all of the above for a cohesive 'joined_info' to display all relevant info
    return kill_info_list + fittings_highs + fittings_mids + fittings_lows


def create_dict_list_from_killids_response(response, num_display):
    to_list = json.loads(response.text)
    to_list = to_list[0:int(num_display)]
    ids = []
    for dicts in to_list:
        ids.append(dicts["killmail_id"])

    return ids


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)