import json
from random import randint

import requests
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = '1234567890'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def get_pilot():
    num_display = request.form.get("num-display")
    num_display = int(num_display)

    if num_display > 200:
        flash('** Please enter an integer from 1 to 200. **')
        return redirect(url_for('index'))

    if request.method == "POST":
        pilot_name = request.form.get("pilot-name")
        mail_type = request.form['action']

        resp = requests.get(f'http://localhost:5001/api/gateway/{pilot_name}/{mail_type}/{num_display}')

        if resp.status_code == 200:
            response = json.loads(resp.text)
            return render_template('killmails.html', mails=response, pilot=pilot_name)
        else:
            print("Error:", resp.status_code)
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/random', methods=['GET', 'POST'])
def get_random():
    num_display = request.form.get("rand-num-display")
    num_display = int(num_display)

    if num_display > 200:
        flash('** Please enter an integer from 1 to 200. **')
        return redirect(url_for('index'))

    if request.method == "POST":
        mail_type = request.form['rand-action']

        # todo: remove and do correctly
        rand_list = []
        for _ in range(100):
            rand_list.append(randint(90000000, 100000000))
        rand_list = json.dumps(rand_list)
        resp = requests.get(f'http://localhost:5001/api/gateway-rand/{rand_list}/{mail_type}/{num_display}')

        if resp.status_code == 200:
            response = json.loads(resp.text)
            return jsonify(response)
        else:
            print("Error:", resp.status_code)
            return redirect(url_for('index'))

    return redirect(url_for('index'))


# @app.route('/killmails')
# def show_killmails():
#     return render_template('killmails.html', mails=mail_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)