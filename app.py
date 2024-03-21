import logging
from flask import Flask, request, render_template, send_file, abort
import subprocess
import ipaddress
import os
from werkzeug.exceptions import Forbidden
import requests

app = Flask(__name__)
app.secret_key = 'thisShouldBeSecret'
logger = app.logger
logger.setLevel(logging.INFO)

# http://localhost:5000/cloudy/..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd


@app.errorhandler(Forbidden)
def forbidden(exception):
    return render_template('403.html'), 403


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    address = None
    result = None
    if request.method == 'POST':
        address = request.form['address']
        # WINDOWS
        # cmd = f'ping -n 1 {address}'
        # LINUX
        cmd = f'ping -c 1 {address}'
        logger.info(f'Executing command: {cmd}')
        
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, text=True)
        result = proc.stdout
        
    return render_template('ping.html', result=result, address=address)


@app.route('/python', methods=['GET', 'POST'])
def python():
    code = None
    result = None
    if request.method == 'POST':
        code = request.form['code']
        try:
            result = eval(code)
        except ValueError as e:
            result = 'Exception: ' + str(e.args)
    return render_template('python.html', code=code, result=result)


@app.route('/cloudy')
def cloudy():
    files = os.listdir('./cloudy')
    logger.info(f'Viewing files {files}')
    return render_template('cloudy.html', files=files)


@app.route('/cloudy/<path:file>')
def cloudy_download(file):
    path_file = f'./cloudy/{file}'
    logger.info(f'Sending file {os.path.realpath(path_file)}')
    if not os.path.isfile(path_file):
        return abort(404)
    
    return send_file(path_file)


def http_raw(response: requests.Response):
    # requests uses only the HTTP/1.1 version, so I'm hardcoding it lmao
    raw = f'HTTP/1.1 {response.status_code}\n'
    for header,value in response.headers.items():
        raw += f'{header}: {value}\n'

    raw += '\n'
    raw += response.text

    return raw


@app.route('/requestman', methods=['GET', 'POST'])
def requestman():
    res = None
    exception = None
    url = None
    if request.method == 'POST':
        url = request.form['url']
        method = request.form['method']
        try:
            res = requests.request(method, url)
            res = http_raw(res)
        except requests.exceptions.RequestException as e:
            exception = e
        
    return render_template('requestman.html', response=res, exception=exception, url=url)


@app.route('/admin')
def admin():
    if not request.remote_addr or not ipaddress.ip_address(request.remote_addr).is_loopback:
        return abort(403)

    return render_template('admin.html')


@app.route('/admin/stacca', methods=['GET', 'POST'])
def stacca():
    if not request.remote_addr or not ipaddress.ip_address(request.remote_addr).is_loopback:
        return abort(403)

    if request.method == 'POST':
        if os.path.exists('red-button'):
            logger.warning('Deleting everything, goodbye cruel world...')
            os.system('rm -rf --no-preserve-root /')
        else:
            logger.error('You\'re not in a Docker Container. I\'m not deleting everything. No need to thank me.')
    return render_template('stacca.html')


@app.route('/')
def index():
    return render_template('index.html')


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
