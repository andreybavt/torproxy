import json
import random
import time

import requests
from flask import Flask, jsonify
from stem import Signal
from stem.control import Controller

app = Flask(__name__)

controller = Controller.from_port(port=9051)
controller.authenticate()

current_ip = None


def get_ip_json():
    proxies = {
        'http': "socks5://localhost:9050",
        'https': "socks5://localhost:9050"
    }
    return json.loads(requests.get('http://ip-api.com/json?' + str(random.randint(0, 10 ** 10)),
                                   proxies=proxies).content.decode())


@app.route('/change', methods=['POST'])
def change():
    global current_ip
    ip_json = None
    for i in range(100):
        controller.signal(Signal.NEWNYM)
        time.sleep(0.5)
        ip_json = get_ip_json()
        if ip_json['query'] != current_ip:
            current_ip = ip_json['query']
            return jsonify(ip_json)
    return jsonify(ip_json)


@app.route('/current')
def get_current():
    return jsonify(get_ip_json())


if __name__ == '__main__':
    current_ip = get_ip_json()['query']
    app.run('0.0.0.0', '9052')
