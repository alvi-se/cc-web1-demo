from flask import Flask, request, render_template
import logging
import subprocess

app = Flask(__name__)
app.secret_key = 'thisShouldBeSecret'
app.debug = True


@app.route('/pinger', methods=['GET', 'POST'])
def pinger():
    address = None
    result = None
    if request.method == 'POST':
        address = request.form['address']
        # WINDOWS
        cmd = f'ping -n 1 {address}'
        # LINUX
        # cmd = f'ping -c 1 {address}'
        print(f'Executing command: {cmd}')
        
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, text=True)
        result = proc.stdout
        
    return render_template('pinger.html', result=result, address=address)


@app.route('/python')
def python():
    return render_template('python.html')


@app.route('/')
def index():
    return render_template('base.html')

def main():
    app.run()


if __name__ == '__main__':
    main()
