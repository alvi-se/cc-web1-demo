from flask import Flask, request, render_template, send_file, abort
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'thisShouldBeSecret'
app.debug = True
logger = app.logger

# http://localhost:5000/cloudy/..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd

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
    print(files)
    return render_template('cloudy.html', files=files)


@app.route('/cloudy/<path:file>')
def cloudy_download(file):
    path_file = f'./cloudy/{file}'
    if not os.path.isfile(path_file):
        abort(404)
    
    return send_file(path_file)


@app.route('/')
def index():
    return render_template('index.html')


def main():
    app.run()


if __name__ == '__main__':
    main()
