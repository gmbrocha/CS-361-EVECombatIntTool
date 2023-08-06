from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/link-svc/<char_id>', methods=['GET'])
def link_service(char_id):
    """
    Receives a char_id int as an argument for the route request, responds with links to relevant sites in a jsonified
    list
    """
    # generate 2 unique links from the char_id int; one for zkillboard.com and the other evewho.com
    zkill_link = f'https://zkillboard.com/character/{char_id}'
    evewho_link = f'https://evewho.com/character/{char_id}'

    return jsonify([zkill_link, evewho_link])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)