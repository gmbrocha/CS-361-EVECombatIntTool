import json
from random import randint

import requests
from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = '1234567890'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def get_pilot():
    """
    route accepts and in input along with a string of a specific pilot for which the # of combat interactions
    """
    # get number of interactions requested
    num_display = request.form.get("num-display")
    num_display = int(num_display)

    # validate for int, zkill requests only give up to 200 items
    validate_number_interactions(num_display)

    # this can be removed, ended up having no get reqs for the route
    if request.method == "POST":

        pilot_name = request.form.get("pilot-name")
        mail_type = request.form.get('action')  # mail type for either 'kills' or 'losses'

        # request to the gateway name, kills/losses, and # of interactions
        resp = requests.get(f'http://localhost:5001/api/gateway/{pilot_name}/{mail_type}/{num_display}')

        # check response from gateway
        response = check_gateway_response_display(resp)
        return render_template('killmails.html', mails=response, pilot=pilot_name, mail_type=mail_type)
    return render_template('index.html')


@app.route('/random', methods=['GET', 'POST'])
def get_random():
    """
    route accepts an int input along with a button submission of kills or losses; validates the # of interactions (max
    that destination API will allow); creates a random list of valid charID ints and passes them to the gateway; returns
    killmail template render with all applicable data from random pilot interactions
    """
    # get number of interactions requested
    num_display = request.form.get("rand-num-display")
    num_display = int(num_display)

    # validate for int, zkill requests only give up to 200 items
    validate_number_interactions(num_display)

    if request.method == "POST":
        mail_type = request.form.get('rand-action')

        # get random list of valid ints to pass for requests until non-empty response is found
        rand_list = create_rand_char_IDs()

        # request to gateway with the random list of valid ints, kills/losses, # of interactions
        resp = requests.get(f'http://localhost:5001/api/gateway-rand/{rand_list}/{mail_type}/{num_display}')

        # check response from gateway
        response = check_rand_gateway_response_display(resp)
        return render_template('killmails.html', mails=response, pilot=response["charName"], mail_type=mail_type)

    return render_template('index.html')


def validate_number_interactions(interactions: int):
    """
    """
    if interactions > 20 or interactions < 1:
        flash('** Please enter an integer from 1 to 20. **')
        return render_template('index.html')


def create_rand_char_IDs():
    """
    """
    rand_list = []
    for _ in range(100):
        rand_list.append(randint(90000000, 98000000))
    return json.dumps(rand_list)


def check_rand_gateway_response_display(response):
    """
    """
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print("Error:", response.status_code)
        return render_template('index.html')


def check_gateway_response_display(response):
    """
    """
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print("Error:", response.status_code)
        return render_template('index.html')


@app.route('/clipboard', methods=['GET', 'POST'])
def clipboard():
    """
    route to handle display of the clipboard notification and to display the back button on successful copy
    """
    return render_template('clip_prev.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)