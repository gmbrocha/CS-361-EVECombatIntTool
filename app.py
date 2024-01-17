import json
from random import randint
import requests
from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = '1234567890'


@app.route('/', methods=['GET', 'POST'])
def get_pilot():
    """
    route accepts and in input along with a string of a specific pilot for which the # of combat interactions
    """
    if request.method == "POST":

        # get requested interactions, validate for, zkill API requests only give up to 20 items
        num_display = int(request.form.get("num-display"))
        if num_display > 20 or num_display < 1:
            flash("**Please enter an integer between 1 and 20**")
            return redirect(url_for('get_pilot'))

        # get pilot name and mail_type (either kills or losses) from submission form
        pilot_name, mail_type = request.form.get("pilot-name"), request.form.get('action')

        # request and check response from gateway
        response = check_gateway_response_display(
            requests.get(f'http://localhost:5001/gateway/{pilot_name}/{mail_type}/{num_display}')
        )
        # return parameters used to populate the killmails div
        return render_template(
            'killmails.html',
            mails=response,
            pilot=pilot_name,
            mail_type=mail_type
        )

    # if GET just render index
    return render_template('index.html')


@app.route('/random', methods=['GET', 'POST'])
def get_random():
    """
    route accepts an int input along with a button submission of kills or losses; validates the # of interactions (max
    that destination API will allow); creates a random list of valid charID ints and passes them to the gateway; returns
    killmail template render with all applicable data from random pilot interactions
    """
    if request.method == "POST":

        # get requested interactions, validate for, zkill API requests only give up to 20 items
        num_display = int(request.form.get("rand-num-display"))
        if num_display > 20 or num_display < 1:
            flash("**Please enter an integer between 1 and 20**")
            return redirect(url_for('get_pilot'))

        # get mail type - either kills or losses
        mail_type = request.form.get('rand-action')

        # request and check response from gateway
        response = check_rand_gateway_response_display(
            requests.get(f'http://localhost:5001/gateway-rand/{create_rand_char_IDs()}/{mail_type}/{num_display}')
        )
        # return parameters used to populate the killmails div
        return render_template('killmails.html',
                               mails=response,
                               pilot=response["charName"],
                               mail_type=mail_type
                               )

    # if GET just render index
    return render_template('index.html')


def create_rand_char_IDs():
    """
    Creates and returns a random 100 element list of valid integers as potential charIDs to request from EVE ESI
    """
    rand_list = []
    for _ in range(100):
        rand_list.append(randint(90000000, 98000000))
    return json.dumps(rand_list)


def check_rand_gateway_response_display(response):
    """
    Redirects back to index (get_pilot) if response is bad
    """
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print("Error:", response.status_code)
        return redirect(url_for('get_pilot'))


def check_gateway_response_display(response):
    """
    Redirects back to index (get_pilot) if response is bad
    """
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print("Error:", response.status_code)
        return redirect(url_for('get_pilot'))


@app.route('/clipboard', methods=['GET', 'POST'])
def clipboard():
    """
    route to handle display of the clipboard notification and to display the back button on successful copy
    """
    return render_template('clip_prev.html')


if __name__ == '__main__':

    # app + services run locally port 5000:5004 inclusive
    app.run(host='0.0.0.0', port=5000)