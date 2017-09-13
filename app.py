import pydeepl

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("metadata").get("intentName") != "translateText":
        return {}

    param = req.get('result').get('parameters')
    text = param.get('text')
    lang = param.get('lang')
    if lang == '':
        lang = 'FR'

    translation = pydeepl.translate(text, lang)
    return {
        "speech": translation,
        "displayText": translation,
        "source": 'translator-deepl-api'
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
