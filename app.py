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

    # get number of interactions requested
    num_display = request.form.get("num-display")
    num_display = int(num_display)

    # validate for int, zkill requests only give up to 200 items
    if num_display > 200 or num_display < 1:

        flash('** Please enter an integer from 1 to 200. **')  # if non-valid, flash message to display at bottom
        return redirect(url_for('index'))

    # this can be removed, ended up having no get reqs for the route
    if request.method == "POST":

        pilot_name = request.form.get("pilot-name")
        mail_type = request.form['action']  # mail type for either 'kills' or 'losses'

        # request to the gateway name, kills/losses, and # of interactions
        resp = requests.get(f'http://localhost:5001/api/gateway/{pilot_name}/{mail_type}/{num_display}')

        if resp.status_code == 200:
            response = json.loads(resp.text)

            # return killmails template with dynamic content (the interaction history)
            return render_template('killmails.html', mails=response, pilot=pilot_name, mail_type=mail_type)
        else:
            print("Error:", resp.status_code)
            return render_template('index.html')
    return render_template('index.html')


@app.route('/random', methods=['GET', 'POST'])
def get_random():

    # get number of interactions requested
    num_display = request.form.get("rand-num-display")
    num_display = int(num_display)

    # validate for int, zkill requests only give up to 200 items
    if num_display > 200 or num_display < 1:
        flash('** Please enter an integer from 1 to 200. **')
        return render_template('index.html')

    if request.method == "POST":

        mail_type = request.form['rand-action']

        # generate list of valid ints to try requests
        rand_list = []
        for _ in range(100):
            rand_list.append(randint(90000000, 100000000))
        rand_list = json.dumps(rand_list)

        # request to gateway with the random list of valid ints, kills/losses, # of interactions
        resp = requests.get(f'http://localhost:5001/api/gateway-rand/{rand_list}/{mail_type}/{num_display}')

        if resp.status_code == 200:

            response = json.loads(resp.text)

            # return killmails template with dynamic content (the interaction history)
            # todo: get pilot_name and pass to render template
            return render_template('killmails.html', mails=response, pilot=response["charid"], mail_type=mail_type)
        else:
            print("Error:", resp.status_code)
            return render_template('index.html')

    return render_template('index.html')


@app.route('/clipboard', methods=['GET', 'POST'])
def clipboard():
    return render_template('clipboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)