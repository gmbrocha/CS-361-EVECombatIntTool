import random
from flask import Flask, jsonify

# create Flask app instance
randState = Flask(__name__)


@randState.route('/random-state', methods=['GET'])
def random_state():
    # list of all state abbrev, not sure if there is really any other way to do this
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
        "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
        "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]

    # generate random index to pull from static states list
    rndIdx = random.randint(0, 49)

    # jsonify the random state string and return to caller
    response = jsonify(states[rndIdx])
    return response


if __name__ == '__main__':

    # designate port for randState app to run
    randState.run(host='0.0.0.0', port=5000)