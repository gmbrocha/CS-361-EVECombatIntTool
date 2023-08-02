import json
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/api/zkill-svc/<charID>/<mail_type>/<num_display>', methods=['GET'])
def zkill_svc(charID, mail_type, num_display):
    kill_hist_endpoint = f"https://zkillboard.com/api/{mail_type}/characterID/{charID}/"

    num_display = int(num_display)

    response = requests.get(kill_hist_endpoint)

    if response.status_code == 200:
        to_list = json.loads(response.text)
        to_list = to_list[0:num_display]
        ids = []
        for dicts in to_list:
            ids.append(dicts["killmail_id"])

        kill_id_endpoint = 'https://zkillboard.com/kill/'

        allmails = {}  # for returning a dict with default of 5 mails

        for idx in ids:
            joined_info = []
            url = kill_id_endpoint + str(idx) + '/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     + '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                       }
            response = requests.get(url, headers=headers)

            kill_info = BeautifulSoup(response.text, 'html.parser')
            title = kill_info.title
            title_to_list = str(title.text).split("|")
            kill_info_list = []
            for i in range(3):
                kill_info_list.append(title_to_list[i].strip())

            fittings_highs = []
            fittings_mids = []
            fittings_lows = []
            for i in range(1, 9):
                highs = kill_info.find("div", {"id": f"high{i}"})
                mids = kill_info.find("div", {"id": f"mid{i}"})
                lows = kill_info.find("div", {"id": f"low{i}"})
                highs = str(highs)
                mids = str(mids)
                lows = str(lows)

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

            joined_info = kill_info_list + fittings_highs + fittings_mids + fittings_lows
            allmails[idx] = joined_info

        return jsonify(allmails)
    else:
        print(f'Error {response.status_code}')
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)