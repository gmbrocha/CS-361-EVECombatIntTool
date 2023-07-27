from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/link-svc/<char_id>', methods=['GET'])
def link_service(char_id):

    zkill_link = f'https://zkillboard.com/character/{char_id}'
    evewho_link = f'https://evewho.com/character/{char_id}'
    links = [zkill_link, evewho_link]

    return jsonify(links)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)