# Server-Side Web Security Demo
A Flask app with stupid-simple web vulnerabilities for demonstration purposes.

The app contains the following services and related vunerability.
- **Ping pong**: it runs a `ping` command on the backend shell and returns the result to the frontend. Vulnerable to command injection.
- **Web Python**: a web Python interpreter, which uses the `eval` function on the backend. Vulnerable to code injection.
- **Cloudy**: provides some file to download. Vulnerable to path traversal.
- **RequestMan**: a very basic API tester. The requests are done on the backend, making it vulnerable to Server-Side Request Forgery.

## Running
Create a Python virtual enviroment and activate it:
```sh
python3 -m venv .venv
source .venv/scripts/activate
```
Install dependencies:
```sh
pip3 install -r requirements.txt
```
Execute the file `app.py`:
```sh
python3 app.py
```
